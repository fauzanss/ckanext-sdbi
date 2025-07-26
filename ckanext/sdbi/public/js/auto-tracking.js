// Auto-tracking JavaScript untuk CKAN SDBI
// Mengirim tracking data secara otomatis ketika halaman dataset diakses

(function ($) {
  'use strict';

  // Track page view ketika halaman dimuat
  $(document).ready(function () {
    // Cek apakah kita berada di halaman dataset
    var currentUrl = window.location.pathname;
    if (currentUrl.indexOf('/dataset/') !== -1) {
      // Extract dataset ID dari URL
      var datasetId = currentUrl.split('/dataset/')[1];
      if (datasetId) {
        // Kirim tracking data
        sendTrackingData(currentUrl, 'page');

        // Update view count dan download count setelah 2 detik
        setTimeout(function () {
          updateViewCount(datasetId);
          updateDownloadCount(datasetId);
        }, 2000);
      }
    }
  });

  function sendTrackingData(url, type) {
    // Kirim POST request ke custom tracking endpoint
    $.ajax({
      url: '/sdbi/tracking',
      method: 'POST',
      data: JSON.stringify({
        url: url,
        type: type
      }),
      contentType: 'application/json',
      dataType: 'json',
      success: function (response) {
        console.log('Auto-tracking successful:', response);
      },
      error: function (xhr, status, error) {
        console.error('Auto-tracking failed:', error);
        // Fallback: coba kirim ke endpoint usertracking jika custom tracking gagal
        sendToUserTracking(url, type);
      }
    });
  }

  function sendToUserTracking(url, type) {
    // Fallback ke usertracking endpoint
    $.ajax({
      url: '/_usertracking',
      method: 'POST',
      data: {
        url: url,
        type: type
      },
      dataType: 'json',
      success: function (response) {
        console.log('UserTracking fallback successful:', response);
      },
      error: function (xhr, status, error) {
        console.error('UserTracking fallback failed:', error);
      }
    });
  }

  function updateViewCount(datasetId) {
    // Update view count dari tracking summary
    $.ajax({
      url: '/api/3/action/package_show',
      method: 'POST',
      data: JSON.stringify({
        id: datasetId,
        include_tracking: true
      }),
      contentType: 'application/json',
      success: function (response) {
        if (response.success && response.result.tracking_summary) {
          var tracking = response.result.tracking_summary;

          // Update total views
          $('.tracking-total-views').text(tracking.total || 0);

          // Update recent views
          $('.tracking-recent-views').text(tracking.recent || 0);

          // Update sidebar views juga
          $('.badge-info .fa-eye').parent().text(tracking.total || 0);
        }
      },
      error: function (xhr, status, error) {
        console.error('Failed to update view count:', error);
      }
    });
  }

  function updateDownloadCount(datasetId) {
    // Get download count using template helper
    $.ajax({
      url: '/api/3/action/package_show',
      method: 'POST',
      data: JSON.stringify({
        id: datasetId
      }),
      contentType: 'application/json',
      success: function (response) {
        if (response.success) {
          var datasetName = response.result.name;

          // Get download count via AJAX call to helper function
          $.ajax({
            url: '/sdbi/downloads/' + datasetName,
            method: 'GET',
            success: function (downloadData) {
              // Update download count display
              $('.tracking-total-downloads').text(downloadData.total_downloads || 0);
              $('.tracking-recent-downloads').text(downloadData.recent_downloads || 0);
              $('.tracking-today-downloads').text(downloadData.today_downloads || 0);

              // Update sidebar downloads juga
              $('.badge-success .fa-download').parent().text(downloadData.total_downloads || 0);
            },
            error: function (xhr, status, error) {
              console.error('Failed to get download count:', error);
            }
          });
        }
      },
      error: function (xhr, status, error) {
        console.error('Failed to get dataset info:', error);
      }
    });
  }

  // Track resource downloads - menggunakan selector yang lebih spesifik
  $(document).on('click', 'a.resource-url-analytics, a[href*="/resource/"], .resource-item a[href*="/resource/"], .btn-group a[href*="/resource/"]', function () {
    var resourceUrl = $(this).attr('href');
    var currentUrl = window.location.pathname;

    if (resourceUrl && currentUrl.indexOf('/dataset/') !== -1) {
      console.log('Download tracking: ' + resourceUrl);
      sendTrackingData(resourceUrl, 'resource');
    }
  });

  // Track setiap 30 detik untuk memastikan tracking data ter-update
  setInterval(function () {
    var currentUrl = window.location.pathname;
    if (currentUrl.indexOf('/dataset/') !== -1) {
      var datasetId = currentUrl.split('/dataset/')[1];
      if (datasetId) {
        updateViewCount(datasetId);
        updateDownloadCount(datasetId);
      }
    }
  }, 30000);

})(jQuery); 