(function () {
  function digitsOnly(value) {
    return String(value || '').replace(/\D/g, '').slice(0, 6);
  }

  function bindCodeInput(input) {
    if (!input) {
      return;
    }
    input.addEventListener('input', function () {
      input.value = digitsOnly(input.value);
    });
    input.addEventListener('paste', function (event) {
      event.preventDefault();
      input.value = digitsOnly((event.clipboardData || window.clipboardData).getData('text'));
    });
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    var field = document.createElement('textarea');
    field.value = text;
    document.body.appendChild(field);
    field.select();
    document.execCommand('copy');
    document.body.removeChild(field);
    return Promise.resolve();
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-copy-secret]');
    if (!button) {
      return;
    }
    var secret = document.getElementById('totp-secret');
    var value = secret ? (secret.textContent || '').trim() : '';
    if (!value) {
      return;
    }
    copyText(value).then(function () {
      var original = button.textContent;
      button.textContent = 'Tersalin';
      button.classList.add('is-copied');
      setTimeout(function () {
        button.textContent = original;
        button.classList.remove('is-copied');
      }, 1600);
    });
  });

  bindCodeInput(document.getElementById('field-mfa'));
})();
