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

        // Update view count setelah 2 detik
        setTimeout(function () {
          updateViewCount(datasetId);
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

  // Track resource downloads
  $(document).on('click', 'a.resource-url-analytics, a.btn-download', function () {
    var resourceUrl = $(this).attr('href');
    var currentUrl = window.location.pathname;

    if (resourceUrl && currentUrl.indexOf('/dataset/') !== -1) {
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
      }
    }
  }, 30000);

})(jQuery); 