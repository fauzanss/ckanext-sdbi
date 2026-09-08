(function () {
  var mapEl = document.getElementById('sebaran-bpbd-map');
  if (!mapEl || typeof maplibregl === 'undefined') {
    return;
  }

  var map = new maplibregl.Map({
    container: 'sebaran-bpbd-map',
    style: 'https://tiles.openfreemap.org/styles/liberty',
    center: [118.0, -2.5],
    zoom: 4.3
  });
  map.addControl(new maplibregl.NavigationControl(), 'top-right');

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

  map.on('load', function () {
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
        });
        map.addLayer({
          id: 'provinsi-line',
          type: 'line',
          source: 'provinsi',
          paint: {
            'line-color': '#206b82',
            'line-width': 1.2
          }
        });
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
          });
          map.addLayer({
            id: 'kabupaten-line',
            type: 'line',
            source: 'kabupaten',
            paint: { 'line-color': '#c05621', 'line-width': 0.6 }
          });
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
        });
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
            'circle-radius': 7,
            'circle-color': '#c53030',
            'circle-stroke-width': 1.5,
            'circle-stroke-color': '#ffffff'
          }
        });
        map.on('click', 'bpbd-points', function (e) {
          var props = e.features[0].properties || {};
          new maplibregl.Popup()
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
