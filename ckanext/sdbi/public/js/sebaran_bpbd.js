(function () {
  var mapEl = document.getElementById('sebaran-bpbd-map');
  if (!mapEl || typeof maplibregl === 'undefined') {
    return;
  }

  var root = document.querySelector('.sebaran-bpbd');
  var map;

  function applyHeaderOffset() {
    var bar = document.querySelector('.sebaran-bpbd__bar');
    var bottom = 0;
    if (bar) {
      bottom = bar.getBoundingClientRect().bottom;
    }
    if (bottom > 0 && root) {
      root.style.setProperty('--sb-header-offset', Math.ceil(bottom) + 'px');
    }
  }

  function syncHeaderOffset() {
    applyHeaderOffset();
    if (map) {
      map.resize();
    }
  }

  applyHeaderOffset();
  map = new maplibregl.Map({
    container: 'sebaran-bpbd-map',
    style: 'https://tiles.openfreemap.org/styles/liberty',
    center: [118.0, -2.5],
    zoom: 4.3,
    attributionControl: false
  });
  map.addControl(new maplibregl.NavigationControl({ visualizePitch: false }), 'top-right');
  map.addControl(new maplibregl.ScaleControl({ maxWidth: 120 }), 'bottom-right');
  syncHeaderOffset();
  window.addEventListener('resize', syncHeaderOffset);

  function applyBpbdData(geojson) {
    var count = ((geojson && geojson.features) || []).length;
    var strong = document.querySelector('.sebaran-bpbd__count strong');
    if (strong) {
      strong.textContent = count;
    }
    if (map && map.getSource('bpbd')) {
      map.getSource('bpbd').setData(geojson);
    }
  }

  function bindImportDialog() {
    var dialog = document.getElementById('sebaran-bpbd-import');
    var openBtn = document.querySelector('.sebaran-bpbd__upload-open');
    if (!dialog || !openBtn || typeof dialog.showModal !== 'function') {
      return;
    }
    var form = dialog.querySelector('.sebaran-bpbd__dialog-form');
    var fileInput = form.querySelector('input[type="file"]');
    var fileLabel = dialog.querySelector('.sebaran-bpbd__drop-file');
    var drop = dialog.querySelector('.sebaran-bpbd__drop');
    var statusEl = dialog.querySelector('.sebaran-bpbd__dialog-status');
    var submitBtn = dialog.querySelector('.sebaran-bpbd__dialog-submit');
    var closeBtns = dialog.querySelectorAll('.sebaran-bpbd__dialog-close, .sebaran-bpbd__dialog-cancel');

    function setStatus(message, kind) {
      statusEl.textContent = message || '';
      statusEl.classList.remove('is-error', 'is-ok');
      if (kind) {
        statusEl.classList.add(kind);
      }
    }

    function resetForm() {
      form.reset();
      fileLabel.textContent = 'Belum ada berkas dipilih';
      submitBtn.disabled = true;
      submitBtn.textContent = 'Impor ke peta';
      setStatus('');
      drop.classList.remove('is-active');
    }

    function closeDialog() {
      if (dialog.open) {
        dialog.close();
      }
    }

    openBtn.addEventListener('click', function () {
      resetForm();
      dialog.showModal();
    });
    closeBtns.forEach(function (btn) {
      btn.addEventListener('click', closeDialog);
    });
    dialog.addEventListener('click', function (event) {
      if (event.target === dialog) {
        closeDialog();
      }
    });
    fileInput.addEventListener('change', function () {
      var file = fileInput.files && fileInput.files[0];
      fileLabel.textContent = file ? file.name : 'Belum ada berkas dipilih';
      submitBtn.disabled = !file;
      setStatus('');
    });
    ['dragenter', 'dragover'].forEach(function (type) {
      drop.addEventListener(type, function (event) {
        event.preventDefault();
        drop.classList.add('is-active');
      });
    });
    ['dragleave', 'drop'].forEach(function (type) {
      drop.addEventListener(type, function (event) {
        event.preventDefault();
        drop.classList.remove('is-active');
      });
    });
    drop.addEventListener('drop', function (event) {
      var files = event.dataTransfer && event.dataTransfer.files;
      if (!files || !files.length) {
        return;
      }
      fileInput.files = files;
      fileInput.dispatchEvent(new Event('change', { bubbles: true }));
    });
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!fileInput.files || !fileInput.files[0]) {
        setStatus('Pilih berkas CSV terlebih dahulu.', 'is-error');
        return;
      }
      submitBtn.disabled = true;
      submitBtn.textContent = 'Mengimpor…';
      setStatus('');
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        credentials: 'same-origin'
      })
        .then(function (res) {
          return res.json().then(function (body) {
            return { ok: res.ok, status: res.status, body: body };
          }).catch(function () {
            throw new Error(res.status === 403
              ? 'Sesi berakhir. Masuk lagi sebagai sysadmin.'
              : 'Impor gagal. Periksa berkas CSV lalu coba lagi.');
          });
        })
        .then(function (result) {
          if (!result.ok || !result.body.success) {
            throw new Error(result.body.error || 'Impor gagal. Periksa berkas CSV lalu coba lagi.');
          }
          setStatus(
            result.body.mapped + ' lokasi terpetakan dari ' + result.body.imported + ' baris.',
            'is-ok'
          );
          return fetch('/sebaran-bpbd/data.geojson').then(function (res) {
            return res.json();
          });
        })
        .then(function (geojson) {
          if (geojson) {
            applyBpbdData(geojson);
          }
          submitBtn.textContent = 'Impor ke peta';
          window.setTimeout(closeDialog, 900);
        })
        .catch(function (err) {
          setStatus(err.message || 'Impor gagal.', 'is-error');
          submitBtn.disabled = false;
          submitBtn.textContent = 'Impor ke peta';
        });
    });
  }
  bindImportDialog();

  function popupHtml(props) {
    var maps = props.maps_url || ('https://www.google.com/maps?q=' + props.lat + ',' + props.lng);
    return (
      '<div class="sebaran-bpbd-popup">' +
      '<h3>' + (props.nama_instansi || 'BPBD') + '</h3>' +
      '<p>' + (props.alamat || '-') + '</p>' +
      '<p><strong>SDM:</strong> ' + (props.jumlah_sdm != null ? props.jumlah_sdm : '-') + '</p>' +
      '<p>' + (props.catatan_sdm || '') + '</p>' +
      '<p><a href="' + maps + '" target="_blank" rel="noopener">Buka di Google Maps</a></p>' +
      '</div>'
    );
  }

  function setVisibility(layerId, visible) {
    if (map.getLayer(layerId)) {
      map.setLayoutProperty(layerId, 'visibility', visible ? 'visible' : 'none');
    }
  }

  function beforePoints() {
    return map.getLayer('bpbd-points') ? 'bpbd-points' : undefined;
  }

  map.on('load', function () {
    map.resize();

    fetch('/data/boundaries/provinsi.geojson')
      .then(function (res) { return res.json(); })
      .then(function (geojson) {
        map.addSource('provinsi', { type: 'geojson', data: geojson });
        map.addLayer({
          id: 'provinsi-fill',
          type: 'fill',
          source: 'provinsi',
          paint: {
            'fill-color': '#206b82',
            'fill-opacity': 0.12
          }
        }, beforePoints());
        map.addLayer({
          id: 'provinsi-line',
          type: 'line',
          source: 'provinsi',
          paint: {
            'line-color': '#206b82',
            'line-width': 1.2
          }
        }, beforePoints());
      })
      .catch(function () {});

    fetch('/data/boundaries/kabupaten.geojson')
      .then(function (res) { return res.ok ? res.json() : null; })
      .then(function (geojson) {
        if (geojson && geojson.features && geojson.features.length) {
          map.addSource('kabupaten', { type: 'geojson', data: geojson });
          map.addLayer({
            id: 'kabupaten-fill',
            type: 'fill',
            source: 'kabupaten',
            paint: { 'fill-color': '#c05621', 'fill-opacity': 0.08 }
          }, beforePoints());
          map.addLayer({
            id: 'kabupaten-line',
            type: 'line',
            source: 'kabupaten',
            paint: { 'line-color': '#c05621', 'line-width': 0.6 }
          }, beforePoints());
          return;
        }
        var sources = map.getStyle().sources || {};
        var vectorId = null;
        Object.keys(sources).forEach(function (id) {
          if (!vectorId && sources[id].type === 'vector') {
            vectorId = id;
          }
        });
        if (!vectorId) return;
        map.addLayer({
          id: 'kabupaten-line',
          type: 'line',
          source: vectorId,
          'source-layer': 'boundary',
          filter: ['all', ['==', ['get', 'admin_level'], 6]],
          paint: { 'line-color': '#c05621', 'line-width': 0.7 }
        }, beforePoints());
      })
      .catch(function () {});

    fetch('/sebaran-bpbd/data.geojson')
      .then(function (res) { return res.json(); })
      .then(function (geojson) {
        map.addSource('bpbd', { type: 'geojson', data: geojson });
        map.addLayer({
          id: 'bpbd-points',
          type: 'circle',
          source: 'bpbd',
          paint: {
            'circle-radius': [
              'interpolate', ['linear'], ['zoom'],
              3, 7,
              6, 9,
              10, 12
            ],
            'circle-color': '#c53030',
            'circle-stroke-width': 1.5,
            'circle-stroke-color': '#ffffff'
          }
        });
        map.on('click', 'bpbd-points', function (e) {
          var props = e.features[0].properties || {};
          new maplibregl.Popup({ closeButton: true, maxWidth: '280px' })
            .setLngLat(e.lngLat)
            .setHTML(popupHtml(props))
            .addTo(map);
        });
        map.on('mouseenter', 'bpbd-points', function () {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'bpbd-points', function () {
          map.getCanvas().style.cursor = '';
        });
      })
      .catch(function () {});
  });

  function bindToggle(checkboxId, layerIds) {
    var el = document.getElementById(checkboxId);
    if (!el) return;
    el.addEventListener('change', function () {
      layerIds.forEach(function (id) {
        setVisibility(id, el.checked);
      });
    });
  }

  bindToggle('layer-provinsi', ['provinsi-fill', 'provinsi-line']);
  bindToggle('layer-kabupaten', ['kabupaten-fill', 'kabupaten-line']);
  bindToggle('layer-bpbd', ['bpbd-points']);
})();
