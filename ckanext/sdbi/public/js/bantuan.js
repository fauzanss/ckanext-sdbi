(function () {
  var input = document.getElementById('bantuan-q');
  var empty = document.getElementById('bantuan-empty');
  if (!input) return;

  function filter() {
    var needle = (input.value || '').trim().toLowerCase();
    var visible = 0;
    document.querySelectorAll('.bantuan__item').forEach(function (item) {
      var hay = ((item.getAttribute('data-q') || '') + ' ' + (item.getAttribute('data-a') || '')).toLowerCase();
      var show = !needle || hay.indexOf(needle) !== -1;
      item.hidden = !show;
      if (show) visible += 1;
    });
    document.querySelectorAll('.bantuan__category').forEach(function (section) {
      var any = section.querySelector('.bantuan__item:not([hidden])');
      section.hidden = !any;
    });
    if (empty) empty.hidden = visible !== 0;
  }

  input.addEventListener('input', filter);
})();
