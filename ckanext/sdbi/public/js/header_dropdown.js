(function () {
  function init() {
    var items = document.querySelectorAll('.site-header .navigation li.dropdown');
    if (!items.length) return;

    Array.prototype.forEach.call(items, function (li) {
      var timer = null;
      var toggle = li.querySelector(':scope > .dropdown-toggle') || li.querySelector('.dropdown-toggle');

      function open() {
        if (timer) {
          window.clearTimeout(timer);
          timer = null;
        }
        li.classList.add('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'true');
      }

      function scheduleClose() {
        if (timer) window.clearTimeout(timer);
        timer = window.setTimeout(function () {
          li.classList.remove('open');
          if (toggle) toggle.setAttribute('aria-expanded', 'false');
          timer = null;
        }, 180);
      }

      li.addEventListener('mouseenter', open);
      li.addEventListener('mouseleave', scheduleClose);
      li.addEventListener('focusin', open);
      li.addEventListener('focusout', function (e) {
        if (!li.contains(e.relatedTarget)) scheduleClose();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
