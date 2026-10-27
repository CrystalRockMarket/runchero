(function () {
  "use strict";

  var filter = document.getElementById("filter");
  var grid = document.getElementById("app-grid");
  var empty = document.getElementById("empty-filter");
  var count = document.getElementById("project-count");
  var cards = grid
    ? Array.prototype.slice.call(grid.querySelectorAll(".app-card:not(.app-card-cta)"))
    : [];

  function applyFilter() {
    if (!filter) return;
    var term = filter.value.trim().toLowerCase();
    var visible = 0;
    cards.forEach(function (card) {
      var haystack = card.getAttribute("data-search") || "";
      var show = !term || haystack.indexOf(term) !== -1;
      card.hidden = !show;
      if (show) visible += 1;
    });
    if (empty) empty.hidden = visible !== 0;
    if (count) count.textContent = String(visible);
  }

  if (filter) {
    filter.addEventListener("input", applyFilter);
    filter.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        filter.value = "";
        applyFilter();
      }
    });
    applyFilter();
  }

  var description = document.getElementById("description");
  var descCount = document.getElementById("desc-count");
  if (description && descCount) {
    var updateCount = function () {
      descCount.textContent = String(description.value.length);
    };
    description.addEventListener("input", updateCount);
    updateCount();
  }

  document.addEventListener("submit", function (event) {
    var form = event.target.closest("form[data-confirm]");
    if (!form) return;
    var message = form.getAttribute("data-confirm") || "Are you sure?";
    if (!window.confirm(message)) {
      event.preventDefault();
    }
  });
})();
