// Smart Exit Intent Detection and Google Forms Popup
// Detects multiple user behaviors and shows Google Forms popup intelligently

(function () {
  'use strict';

  // Enhanced Configuration
  const SMART_EXIT_INTENT_CONFIG = {
    // Basic settings
    threshold: 10, // Distance from top edge to trigger exit intent
    delay: 1000,   // Delay before showing popup (ms)
    cookieName: 'smart_exit_intent_shown',
    cookieExpiry: 1, // Days
    debug: true,

    // Smart triggers configuration
    enableMouseExit: true,           // Mouse movement to top
    enableKeyboardShortcuts: true,   // Cmd+W, Cmd+Q, Alt+F4 detection
    enableEscapeKey: true,           // Escape key detection
    enableTabSwitch: true,           // Tab switching detection
    enableFocusLoss: true,           // Focus loss detection

    // NEW: Smart triggers
    enableScrollBased: true,         // Show form when scrolling near bottom
    enableTimeBased: true,           // Show form after X minutes on page
    enableInactivityBased: true,     // Show form after X seconds of inactivity
    enableClickBased: true,          // Show form when clicking external links

    // Timing thresholds (in milliseconds)
    escapeKeyDelay: 5000,           // Minimum time before Escape key triggers
    tabSwitchDelay: 10000,          // Minimum time before tab switch triggers
    focusLossDelay: 15000,          // Minimum time before focus loss triggers
    timeBasedDelay: 180000,         // Show form after 3 minutes (180 seconds)
    inactivityDelay: 30000,         // Show form after 30 seconds of inactivity
    scrollThreshold: 0.8,           // Show form when 80% of page is scrolled

    // Firefox-specific configuration
    enableFirefoxWorkaround: true,
    firefoxReturnDelay: 5000,

    // Smart behavior
    maxTriggersPerSession: 2,       // Maximum times to show form per session
    sessionDuration: 3600000,       // Session duration (1 hour)
    triggerCooldown: 300000,        // 5 minutes cooldown between triggers
  };

  let exitIntentTriggered = false;
  let popupShown = false;
  let triggerCount = 0;
  let lastTriggerTime = 0;
  let sessionStartTime = Date.now();
  let inactivityTimer = null;
  let timeBasedTimer = null;
  let pageLoadTime = Date.now();

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

  // Create enhanced popup modal with better UX
  function createPopupModal(form) {
    const modal = document.createElement('div');
    modal.className = 'smart-exit-intent-modal';
    modal.innerHTML = `
      <div class="smart-exit-intent-overlay"></div>
      <div class="smart-exit-intent-content">
        <div class="smart-exit-intent-header">
          <div class="header-content">
            <h3><i class="fa fa-heart"></i> ${form.title}</h3>
            <p class="header-subtitle">Kami menghargai waktu Anda!</p>
          </div>
          <button class="smart-exit-intent-close" onclick="closeSmartExitIntentModal()">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div class="smart-exit-intent-body">
          <div class="form-description">
            <p>${form.description || 'Sebelum Anda melanjutkan, mohon berikan feedback singkat untuk membantu kami meningkatkan layanan.'}</p>
          </div>
          <div class="smart-exit-intent-iframe-container">
            <iframe src="${form.form_url}" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
        <div class="smart-exit-intent-footer">
          <div class="footer-actions">
            <button class="btn btn-secondary" onclick="closeSmartExitIntentModal()">
              <i class="fa fa-times"></i> Tutup
            </button>
            <a href="${form.form_url}" target="_blank" class="btn btn-primary">
              <i class="fa fa-external-link"></i> Buka di Tab Baru
            </a>
          </div>
          <div class="footer-note">
            <small><i class="fa fa-info-circle"></i> Form ini hanya membutuhkan waktu 1-2 menit</small>
          </div>
        </div>
      </div>
    `;
    return modal;
  }

  // Show enhanced popup modal
  function showPopupModal(form) {
    if (popupShown) return;

    // Use existing modal from footer
    if (typeof showSurveyPopup === 'function') {
      showSurveyPopup();
    } else {
      // Fallback: create and show the modal
      const modal = createPopupModal(form);
      document.body.appendChild(modal);

      // Add enhanced CSS if not already added
      if (!document.getElementById('smart-exit-intent-styles')) {
        const style = document.createElement('style');
        style.id = 'smart-exit-intent-styles';
        style.textContent = `
        .smart-exit-intent-modal {
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

        .smart-exit-intent-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.7);
          backdrop-filter: blur(5px);
        }

        .smart-exit-intent-content {
          position: relative;
          background: white;
          border-radius: 12px;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
          max-width: 90vw;
          max-height: 90vh;
          width: 600px;
          overflow: hidden;
          animation: slideIn 0.3s ease-out;
        }

        .smart-exit-intent-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }

        .header-content h3 {
          margin: 0 0 5px 0;
          font-size: 18px;
          font-weight: 600;
        }

        .header-subtitle {
          margin: 0;
          font-size: 14px;
          opacity: 0.9;
        }

        .smart-exit-intent-close {
          background: none;
          border: none;
          color: white;
          font-size: 20px;
          cursor: pointer;
          padding: 5px;
          border-radius: 50%;
          transition: background 0.3s;
        }

        .smart-exit-intent-close:hover {
          background: rgba(255, 255, 255, 0.2);
        }

        .smart-exit-intent-body {
          padding: 20px;
          max-height: 60vh;
          overflow-y: auto;
        }

        .form-description {
          margin-bottom: 15px;
          padding: 15px;
          background: #f8f9fa;
          border-radius: 8px;
          border-left: 4px solid #007bff;
        }

        .form-description p {
          margin: 0;
          color: #495057;
          line-height: 1.5;
        }

        .smart-exit-intent-iframe-container {
          border: 1px solid #dee2e6;
          border-radius: 8px;
          overflow: hidden;
        }

        .smart-exit-intent-iframe-container iframe {
          width: 100%;
          height: 400px;
          border: none;
        }

        .smart-exit-intent-footer {
          padding: 15px 20px;
          background: #f8f9fa;
          border-top: 1px solid #dee2e6;
        }

        .footer-actions {
          display: flex;
          gap: 10px;
          margin-bottom: 10px;
        }

        .footer-note {
          text-align: center;
          color: #6c757d;
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes slideIn {
          from { transform: translateY(-50px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }

        @keyframes fadeOut {
          from { opacity: 1; }
          to { opacity: 0; }
        }

        @media (max-width: 768px) {
          .smart-exit-intent-content {
            width: 95vw;
            margin: 10px;
          }
          
          .smart-exit-intent-iframe-container iframe {
            height: 300px;
          }
          
          .footer-actions {
            flex-direction: column;
          }
        }
      `;
        document.head.appendChild(style);
      }
    }

    popupShown = true;
    setCookie(SMART_EXIT_INTENT_CONFIG.cookieName, 'true', SMART_EXIT_INTENT_CONFIG.cookieExpiry);

    if (SMART_EXIT_INTENT_CONFIG.debug) {
      console.log('Smart exit intent popup shown for form:', form.title);
    }
  }

  // Close enhanced popup modal
  window.closeSmartExitIntentModal = function () {
    const modal = document.querySelector('.smart-exit-intent-modal');
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

  // Smart trigger validation
  function canTriggerExitIntent() {
    if (exitIntentTriggered || popupShown) return false;

    // Check session limits
    const sessionElapsed = Date.now() - sessionStartTime;
    if (sessionElapsed > SMART_EXIT_INTENT_CONFIG.sessionDuration) {
      sessionStartTime = Date.now();
      triggerCount = 0;
    }

    if (triggerCount >= SMART_EXIT_INTENT_CONFIG.maxTriggersPerSession) {
      return false;
    }

    // Check cooldown
    const timeSinceLastTrigger = Date.now() - lastTriggerTime;
    if (timeSinceLastTrigger < SMART_EXIT_INTENT_CONFIG.triggerCooldown) {
      return false;
    }

    // Check cookie
    if (getCookie(SMART_EXIT_INTENT_CONFIG.cookieName)) {
      return false;
    }

    return true;
  }

  // Enhanced exit intent trigger function
  function triggerExitIntent(triggerType = 'unknown') {
    if (!canTriggerExitIntent()) return;

    exitIntentTriggered = true;
    triggerCount++;
    lastTriggerTime = Date.now();

    if (SMART_EXIT_INTENT_CONFIG.debug) {
      console.log(`Smart exit intent triggered by: ${triggerType}`);
    }

    // Get exit intent forms and show popup
    getExitIntentForms().then(forms => {
      if (forms.length > 0) {
        const form = forms[0];
        setTimeout(() => {
          showPopupModal(form);
        }, SMART_EXIT_INTENT_CONFIG.delay);
      }
    });
  }

  // NEW: Scroll-based exit intent
  function handleScrollBasedExitIntent() {
    if (!SMART_EXIT_INTENT_CONFIG.enableScrollBased) return;

    const scrollPercentage = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
    if (scrollPercentage >= SMART_EXIT_INTENT_CONFIG.scrollThreshold) {
      triggerExitIntent('scroll');
    }
  }

  // NEW: Time-based exit intent
  function handleTimeBasedExitIntent() {
    if (!SMART_EXIT_INTENT_CONFIG.enableTimeBased) return;

    const timeOnPage = Date.now() - pageLoadTime;
    if (timeOnPage >= SMART_EXIT_INTENT_CONFIG.timeBasedDelay) {
      triggerExitIntent('time');
    }
  }

  // NEW: Inactivity-based exit intent
  function resetInactivityTimer() {
    if (inactivityTimer) {
      clearTimeout(inactivityTimer);
    }

    if (SMART_EXIT_INTENT_CONFIG.enableInactivityBased) {
      inactivityTimer = setTimeout(() => {
        triggerExitIntent('inactivity');
      }, SMART_EXIT_INTENT_CONFIG.inactivityDelay);
    }
  }

  // NEW: Click-based exit intent
  function handleClickBasedExitIntent(e) {
    if (!SMART_EXIT_INTENT_CONFIG.enableClickBased) return;

    const target = e.target.closest('a');
    if (target && target.href) {
      const url = new URL(target.href);
      const currentUrl = new URL(window.location.href);

      // Check if it's an external link
      if (url.hostname !== currentUrl.hostname) {
        triggerExitIntent('click');
      }
    }
  }

  // Original exit intent handlers (enhanced)
  function handleMouseExitIntent(e) {
    if (!SMART_EXIT_INTENT_CONFIG.enableMouseExit) return;

    if (e.clientY <= SMART_EXIT_INTENT_CONFIG.threshold) {
      triggerExitIntent('mouse');
    }
  }

  function handleKeyboardExitIntent(e) {
    if (!SMART_EXIT_INTENT_CONFIG.enableKeyboardShortcuts && !SMART_EXIT_INTENT_CONFIG.enableEscapeKey) return;

    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const cmdKey = isMac ? e.metaKey : e.ctrlKey;

    // Keyboard shortcuts - using safer combinations that don't conflict with browser
    if (SMART_EXIT_INTENT_CONFIG.enableKeyboardShortcuts) {
      // Safe shortcuts that won't close the browser
      if ((cmdKey && e.key === 'q') || (cmdKey && e.key === 'x') || (e.altKey && e.key === 'F4')) {
        e.preventDefault();
        e.stopPropagation();
        triggerExitIntent('keyboard');
        return;
      }

      // Cmd+W alternative - use Cmd+Shift+W instead
      if (cmdKey && e.shiftKey && e.key === 'W') {
        e.preventDefault();
        e.stopPropagation();
        triggerExitIntent('keyboard');
        return;
      }

      // Additional safe shortcuts
      if ((cmdKey && e.key === 'E') || (cmdKey && e.key === 'R') || (cmdKey && e.key === 'T')) {
        e.preventDefault();
        e.stopPropagation();
        triggerExitIntent('keyboard');
        return;
      }

      // macOS specific - hide/minimize
      if (isMac && ((e.metaKey && e.key === 'h') || (e.metaKey && e.key === 'm'))) {
        e.preventDefault();
        e.stopPropagation();
        triggerExitIntent('keyboard');
        return;
      }
    }

    // Escape key
    if (SMART_EXIT_INTENT_CONFIG.enableEscapeKey && e.key === 'Escape') {
      if (Date.now() - pageLoadTime > SMART_EXIT_INTENT_CONFIG.escapeKeyDelay) {
        triggerExitIntent('escape');
      }
    }
  }

  function handleVisibilityChange() {
    if (!SMART_EXIT_INTENT_CONFIG.enableTabSwitch) return;

    if (Date.now() - pageLoadTime > SMART_EXIT_INTENT_CONFIG.tabSwitchDelay) {
      if (document.hidden) {
        triggerExitIntent('tab_switch');
      }
    }
  }

  function handleFocusLoss() {
    if (!SMART_EXIT_INTENT_CONFIG.enableFocusLoss) return;

    if (Date.now() - pageLoadTime > SMART_EXIT_INTENT_CONFIG.focusLossDelay) {
      triggerExitIntent('focus_loss');
    }
  }

  // Initialize smart exit intent detection
  function initSmartExitIntent() {
    if (window.smartExitIntentInitialized) return;

    // Check if we should show exit intent (not on admin pages)
    const currentPath = window.location.pathname;
    if (currentPath.includes('/google-forms') || currentPath.includes('/admin')) {
      if (SMART_EXIT_INTENT_CONFIG.debug) {
        console.log('Smart exit intent disabled on admin pages');
      }
      return;
    }

    // Add event listeners for different triggers
    if (SMART_EXIT_INTENT_CONFIG.enableMouseExit) {
      document.addEventListener('mouseleave', handleMouseExitIntent);
      document.addEventListener('mouseout', handleMouseExitIntent);
    }

    if (SMART_EXIT_INTENT_CONFIG.enableKeyboardShortcuts || SMART_EXIT_INTENT_CONFIG.enableEscapeKey) {
      document.addEventListener('keydown', handleKeyboardExitIntent);
    }

    if (SMART_EXIT_INTENT_CONFIG.enableTabSwitch) {
      document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    if (SMART_EXIT_INTENT_CONFIG.enableFocusLoss) {
      window.addEventListener('blur', handleFocusLoss);
    }

    // NEW: Smart triggers
    if (SMART_EXIT_INTENT_CONFIG.enableScrollBased) {
      window.addEventListener('scroll', handleScrollBasedExitIntent);
    }

    if (SMART_EXIT_INTENT_CONFIG.enableClickBased) {
      document.addEventListener('click', handleClickBasedExitIntent);
    }

    // Initialize inactivity timer
    resetInactivityTimer();

    // Add activity listeners for inactivity detection
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
      document.addEventListener(event, resetInactivityTimer, true);
    });

    // Set up time-based trigger
    if (SMART_EXIT_INTENT_CONFIG.enableTimeBased) {
      timeBasedTimer = setTimeout(handleTimeBasedExitIntent, SMART_EXIT_INTENT_CONFIG.timeBasedDelay);
    }

    window.smartExitIntentInitialized = true;

    if (SMART_EXIT_INTENT_CONFIG.debug) {
      console.log('Smart exit intent detection initialized');
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSmartExitIntent);
  } else {
    initSmartExitIntent();
  }

  // Also initialize after a short delay to ensure all scripts are loaded
  setTimeout(initSmartExitIntent, 1000);

})(); 