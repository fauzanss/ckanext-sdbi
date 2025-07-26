// Exit Intent Detection and Google Forms Popup
// Detects when user is about to leave the page and shows Google Forms popup

(function () {
  'use strict';

  // Configuration
  const EXIT_INTENT_CONFIG = {
    threshold: 10, // Distance from top edge to trigger exit intent
    delay: 1000,   // Delay before showing popup (ms)
    cookieName: 'exit_intent_shown',
    cookieExpiry: 1, // Days
    debug: false,
    // New features configuration
    enableKeyboardShortcuts: true,  // Enable Cmd+W, Cmd+Q, Alt+F4 detection
    enableEscapeKey: true,          // Enable Escape key detection
    enableTabSwitch: true,          // Enable tab switching detection
    enableFocusLoss: true,          // Enable focus loss detection
    // Firefox-specific configuration
    enableFirefoxWorkaround: true,  // Enable Firefox-specific workarounds
    firefoxReturnDelay: 5000,       // Time window to detect return from Cmd+W (ms)
    // Timing thresholds (in milliseconds)
    escapeKeyDelay: 5000,           // Minimum time before Escape key triggers
    tabSwitchDelay: 10000,          // Minimum time before tab switch triggers
    focusLossDelay: 15000           // Minimum time before focus loss triggers
  };

  let exitIntentTriggered = false;
  let popupShown = false;

  // Get Google Forms with exit intent enabled
  function getExitIntentForms() {
    return fetch('/api/google-forms/exit-intent')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          return data.forms;
        }
        return [];
      })
      .catch(error => {
        console.error('Error fetching exit intent forms:', error);
        return [];
      });
  }

  // Create popup modal
  function createPopupModal(form) {
    const modal = document.createElement('div');
    modal.className = 'exit-intent-modal';
    modal.innerHTML = `
      <div class="exit-intent-overlay"></div>
      <div class="exit-intent-content">
        <div class="exit-intent-header">
          <h3><i class="fa fa-exclamation-triangle"></i> ${form.title}</h3>
          <button class="exit-intent-close" onclick="closeExitIntentModal()">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div class="exit-intent-body">
          <p>${form.description || 'Mohon isi form ini sebelum Anda meninggalkan halaman.'}</p>
          <div class="exit-intent-iframe-container">
            <iframe src="${form.form_url}" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
        <div class="exit-intent-footer">
          <button class="btn btn-secondary" onclick="closeExitIntentModal()">
            <i class="fa fa-times"></i> Tutup
          </button>
          <a href="${form.form_url}" target="_blank" class="btn btn-primary">
            <i class="fa fa-external-link"></i> Buka di Tab Baru
          </a>
        </div>
      </div>
    `;
    return modal;
  }

  // Show popup modal
  function showPopupModal(form) {
    if (popupShown) return;

    const modal = createPopupModal(form);
    document.body.appendChild(modal);

    // Add CSS for modal
    if (!document.getElementById('exit-intent-styles')) {
      const style = document.createElement('style');
      style.id = 'exit-intent-styles';
      style.textContent = `
        .exit-intent-modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 9999;
          display: flex;
          align-items: center;
          justify-content: center;
          animation: fadeIn 0.3s ease-in-out;
        }

        .exit-intent-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.7);
          backdrop-filter: blur(5px);
        }

        .exit-intent-content {
          position: relative;
          background: white;
          border-radius: 12px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
          max-width: 90vw;
          max-height: 90vh;
          width: 600px;
          overflow: hidden;
          animation: slideIn 0.3s ease-out;
        }

        .exit-intent-header {
          background: #f8f9fa;
          padding: 1rem 1.5rem;
          border-bottom: 1px solid #e9ecef;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .exit-intent-header h3 {
          margin: 0;
          color: #333;
          font-size: 1.2rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .exit-intent-header h3 i {
          color: #ffc107;
        }

        .exit-intent-close {
          background: none;
          border: none;
          font-size: 1.5rem;
          color: #6c757d;
          cursor: pointer;
          padding: 0;
          width: 30px;
          height: 30px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: all 0.3s ease;
        }

        .exit-intent-close:hover {
          background: #e9ecef;
          color: #333;
        }

        .exit-intent-body {
          padding: 1.5rem;
          max-height: 60vh;
          overflow-y: auto;
        }

        .exit-intent-body p {
          margin-bottom: 1rem;
          color: #666;
          line-height: 1.5;
        }

        .exit-intent-iframe-container {
          border: 1px solid #e9ecef;
          border-radius: 8px;
          overflow: hidden;
          margin-bottom: 1rem;
        }

        .exit-intent-iframe-container iframe {
          width: 100%;
          height: 400px;
          border: none;
        }

        .exit-intent-footer {
          background: #f8f9fa;
          padding: 1rem 1.5rem;
          border-top: 1px solid #e9ecef;
          display: flex;
          gap: 0.75rem;
          justify-content: flex-end;
        }

        .exit-intent-footer .btn {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-weight: 500;
          transition: all 0.3s ease;
        }

        .btn-secondary {
          background: #6c757d;
          color: white;
          border: 1px solid #6c757d;
        }

        .btn-secondary:hover {
          background: #5a6268;
          border-color: #545b62;
          color: white;
        }

        .btn-primary {
          background: #007bff;
          color: white;
          border: 1px solid #007bff;
        }

        .btn-primary:hover {
          background: #0056b3;
          border-color: #0056b3;
          color: white;
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes slideIn {
          from { 
            opacity: 0;
            transform: translateY(-50px) scale(0.9);
          }
          to { 
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        @media (max-width: 768px) {
          .exit-intent-content {
            width: 95vw;
            max-height: 95vh;
          }

          .exit-intent-iframe-container iframe {
            height: 300px;
          }

          .exit-intent-footer {
            flex-direction: column;
          }

          .exit-intent-footer .btn {
            justify-content: center;
          }
        }
      `;
      document.head.appendChild(style);
    }

    popupShown = true;
    setCookie(EXIT_INTENT_CONFIG.cookieName, 'true', EXIT_INTENT_CONFIG.cookieExpiry);

    if (EXIT_INTENT_CONFIG.debug) {
      console.log('Exit intent popup shown for form:', form.title);
    }
  }

  // Close popup modal
  window.closeExitIntentModal = function () {
    const modal = document.querySelector('.exit-intent-modal');
    if (modal) {
      modal.style.animation = 'fadeOut 0.3s ease-in-out';
      setTimeout(() => {
        if (modal.parentNode) {
          modal.parentNode.removeChild(modal);
        }
      }, 300);
    }
  };

  // Cookie utilities
  function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
  }

  function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  // Exit intent detection for mouse movement
  function handleMouseExitIntent(e) {
    if (exitIntentTriggered || popupShown) return;

    // Check if user is moving mouse towards the top of the page
    if (e.clientY <= EXIT_INTENT_CONFIG.threshold) {
      triggerExitIntent();
    }
  }

  // Exit intent detection for keyboard shortcuts
  function handleKeyboardExitIntent(e) {
    if (exitIntentTriggered || popupShown) return;

    // Detect common exit shortcuts
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const cmdKey = isMac ? e.metaKey : e.ctrlKey;

    // Cmd+W (close tab) or Ctrl+W - Note: Firefox may not allow preventDefault
    if (EXIT_INTENT_CONFIG.enableKeyboardShortcuts && cmdKey && e.key === 'w') {
      e.preventDefault();
      e.stopPropagation();
      triggerExitIntent();
      return;
    }

    // Cmd+Q (quit browser) or Ctrl+Q
    if (EXIT_INTENT_CONFIG.enableKeyboardShortcuts && cmdKey && e.key === 'q') {
      e.preventDefault();
      e.stopPropagation();
      triggerExitIntent();
      return;
    }

    // Cmd+X (cut - sometimes used to close) or Ctrl+X
    if (EXIT_INTENT_CONFIG.enableKeyboardShortcuts && cmdKey && e.key === 'x') {
      e.preventDefault();
      e.stopPropagation();
      triggerExitIntent();
      return;
    }

    // Alt+F4 (Windows close window)
    if (EXIT_INTENT_CONFIG.enableKeyboardShortcuts && e.altKey && e.key === 'F4') {
      e.preventDefault();
      e.stopPropagation();
      triggerExitIntent();
      return;
    }

    // Escape key (common exit key)
    if (EXIT_INTENT_CONFIG.enableEscapeKey && e.key === 'Escape') {
      // Only trigger if user has been on page for more than configured time
      if (Date.now() - pageLoadTime > EXIT_INTENT_CONFIG.escapeKeyDelay) {
        triggerExitIntent();
      }
      return;
    }

    // Additional macOS shortcuts
    if (isMac && EXIT_INTENT_CONFIG.enableKeyboardShortcuts) {
      // Cmd+H (hide window)
      if (e.metaKey && e.key === 'h') {
        e.preventDefault();
        e.stopPropagation();
        triggerExitIntent();
        return;
      }

      // Cmd+M (minimize window)
      if (e.metaKey && e.key === 'm') {
        e.preventDefault();
        e.stopPropagation();
        triggerExitIntent();
        return;
      }
    }
  }

  // Enhanced beforeunload handler for Firefox and other browsers
  function handleBeforeUnload(e) {
    if (!exitIntentTriggered && !popupShown) {
      getExitIntentForms().then(forms => {
        if (forms.length > 0 && !getCookie(EXIT_INTENT_CONFIG.cookieName)) {
          // Show a simple confirmation dialog
          e.preventDefault();
          e.returnValue = 'Apakah Anda yakin ingin meninggalkan halaman ini?';
          return e.returnValue;
        }
      });
    }
  }

  // Pagehide handler for Firefox (when preventDefault doesn't work)
  function handlePageHide(e) {
    if (!exitIntentTriggered && !popupShown) {
      // This is a last resort - the page is actually leaving
      // We can't prevent it, but we can track it
      if (EXIT_INTENT_CONFIG.debug) {
        console.log('Page is leaving - exit intent triggered via pagehide');
      }

      // Store in sessionStorage that user tried to leave
      sessionStorage.setItem('exit_intent_attempted', 'true');
      sessionStorage.setItem('exit_intent_timestamp', Date.now().toString());
    }
  }

    // Check for previous exit intent attempts on page load
  function checkPreviousExitIntent() {
    if (!EXIT_INTENT_CONFIG.enableFirefoxWorkaround) return;
    
    const attempted = sessionStorage.getItem('exit_intent_attempted');
    const timestamp = sessionStorage.getItem('exit_intent_timestamp');
    
    if (attempted === 'true' && timestamp) {
      const timeDiff = Date.now() - parseInt(timestamp);
      // If user returned within configured time, show popup
      if (timeDiff < EXIT_INTENT_CONFIG.firefoxReturnDelay) {
        getExitIntentForms().then(forms => {
          if (forms.length > 0 && !getCookie(EXIT_INTENT_CONFIG.cookieName)) {
            setTimeout(() => {
              showPopupModal(forms[0]);
            }, 1000);
          }
        });
      }
      
      // Clear the flag
      sessionStorage.removeItem('exit_intent_attempted');
      sessionStorage.removeItem('exit_intent_timestamp');
    }
  }

  // Track keyboard activity to detect potential exit intent
  let lastKeyPressTime = 0;
  let keyPressCount = 0;

  function handleKeyPress(e) {
    if (exitIntentTriggered || popupShown) return;

    const now = Date.now();
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const cmdKey = isMac ? e.metaKey : e.ctrlKey;

    // Track Cmd+W or Ctrl+W attempts
    if (cmdKey && e.key === 'w') {
      keyPressCount++;
      lastKeyPressTime = now;

      // If user tries Cmd+W multiple times quickly, trigger exit intent
      if (keyPressCount >= 2 && (now - lastKeyPressTime) < 2000) {
        triggerExitIntent();
      }
    }
  }

  // Exit intent detection for visibility change (tab switching)
  function handleVisibilityChange() {
    if (exitIntentTriggered || popupShown) return;

    if (EXIT_INTENT_CONFIG.enableTabSwitch) {
      // Only trigger if user has been on page for more than configured time
      if (Date.now() - pageLoadTime > EXIT_INTENT_CONFIG.tabSwitchDelay) {
        if (document.hidden) {
          triggerExitIntent();
        }
      }
    }
  }

  // Exit intent detection for focus loss
  function handleFocusLoss() {
    if (exitIntentTriggered || popupShown) return;

    if (EXIT_INTENT_CONFIG.enableFocusLoss) {
      // Only trigger if user has been on page for more than configured time
      if (Date.now() - pageLoadTime > EXIT_INTENT_CONFIG.focusLossDelay) {
        triggerExitIntent();
      }
    }
  }

  // Main exit intent trigger function
  function triggerExitIntent() {
    if (exitIntentTriggered || popupShown) return;

    exitIntentTriggered = true;

    // Check if popup was already shown today
    if (getCookie(EXIT_INTENT_CONFIG.cookieName)) {
      if (EXIT_INTENT_CONFIG.debug) {
        console.log('Exit intent popup already shown today');
      }
      return;
    }

    // Get exit intent forms and show popup
    getExitIntentForms().then(forms => {
      if (forms.length > 0) {
        // Show first form (can be enhanced to show random form or based on priority)
        const form = forms[0];
        setTimeout(() => {
          showPopupModal(form);
        }, EXIT_INTENT_CONFIG.delay);
      }
    });
  }

  // Track page load time
  let pageLoadTime = Date.now();

  // Initialize exit intent detection
  function initExitIntent() {
    // Only initialize if not already done
    if (window.exitIntentInitialized) return;

    // Check if we should show exit intent (not on admin pages)
    const currentPath = window.location.pathname;
    if (currentPath.includes('/google-forms') || currentPath.includes('/admin')) {
      if (EXIT_INTENT_CONFIG.debug) {
        console.log('Exit intent disabled on admin pages');
      }
      return;
    }

    // Add event listeners for different exit intent triggers
    document.addEventListener('mouseleave', handleMouseExitIntent);
    document.addEventListener('mouseout', handleMouseExitIntent);

    // Keyboard shortcuts detection
    if (EXIT_INTENT_CONFIG.enableKeyboardShortcuts || EXIT_INTENT_CONFIG.enableEscapeKey) {
      document.addEventListener('keydown', handleKeyboardExitIntent);
      document.addEventListener('keypress', handleKeyPress);
    }

    // Visibility change detection (tab switching)
    if (EXIT_INTENT_CONFIG.enableTabSwitch) {
      document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    // Focus loss detection
    if (EXIT_INTENT_CONFIG.enableFocusLoss) {
      window.addEventListener('blur', handleFocusLoss);
    }

    // Enhanced beforeunload handler for Firefox and other browsers
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Pagehide handler for Firefox (when preventDefault doesn't work)
    window.addEventListener('pagehide', handlePageHide);

    window.exitIntentInitialized = true;

    // Check for previous exit intent attempts
    checkPreviousExitIntent();

    if (EXIT_INTENT_CONFIG.debug) {
      console.log('Exit intent detection initialized');
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initExitIntent);
  } else {
    initExitIntent();
  }

  // Also initialize after a short delay to ensure all scripts are loaded
  setTimeout(initExitIntent, 1000);

})(); 