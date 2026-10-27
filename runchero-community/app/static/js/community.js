(function () {
  "use strict";

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
