/* Runchero Information Depo - progressive enhancement.
   Everything works without JavaScript; this only adds live search. */
(function () {
  "use strict";

  var input = document.querySelector("[data-search]");
  var box = document.getElementById("suggestions");
  if (!input || !box) { return; }

  var timer = null;
  var items = [];
  var cursor = -1;

  function close() {
    box.classList.remove("open");
    box.innerHTML = "";
    items = [];
    cursor = -1;
  }

  function render(results) {
    if (!results.length) { close(); return; }
    var html = "";
    for (var i = 0; i < results.length; i++) {
      var r = results[i];
      var kind = r.kind === "book" ? "BOOK" : "NOTE";
      html += '<a href="' + r.url + '"><span class="kind">' + kind + "</span>" +
              escapeHtml(r.title) + "</a>";
    }
    box.innerHTML = html;
    box.classList.add("open");
    items = Array.prototype.slice.call(box.querySelectorAll("a"));
    cursor = -1;
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function fetchResults(term) {
    var request = new XMLHttpRequest();
    request.open("GET", "/api/search?q=" + encodeURIComponent(term), true);
    request.onload = function () {
      if (request.status !== 200) { close(); return; }
      try {
        render((JSON.parse(request.responseText).results) || []);
      } catch (err) { close(); }
    };
    request.onerror = close;
    request.send();
  }

  input.addEventListener("input", function () {
    var term = input.value.trim();
    clearTimeout(timer);
    if (term.length < 2) { close(); return; }
    timer = setTimeout(function () { fetchResults(term); }, 140);
  });

  input.addEventListener("focus", function () {
    if (input.value.trim().length >= 2) { fetchResults(input.value.trim()); }
  });

  input.addEventListener("keydown", function (event) {
    if (event.key === "Escape") { close(); input.blur(); return; }
    if (!items.length) { return; }
    if (event.key === "ArrowDown") {
      event.preventDefault();
      cursor = (cursor + 1) % items.length;
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      cursor = (cursor - 1 + items.length) % items.length;
    } else if (event.key === "Enter" && cursor >= 0) {
      event.preventDefault();
      window.location.href = items[cursor].getAttribute("href");
      return;
    }
    for (var i = 0; i < items.length; i++) {
      items[i].classList.remove("sel");
    }
    if (cursor >= 0) { items[cursor].classList.add("sel"); }
  });

  document.addEventListener("click", function (event) {
    if (!box.contains(event.target) && event.target !== input) { close(); }
  });

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () { /* offline only */ });
    });
  }
})();

/* Live filters for long shelf and cookbook lists. */
(function () {
  "use strict";
  var inputs = document.querySelectorAll("[data-list-filter]");
  for (var i = 0; i < inputs.length; i++) {
    (function (input) {
      var key = input.getAttribute("data-list-filter");
      var rows = document.querySelectorAll('[data-list="' + key + '"] [data-filter-text]');
      input.addEventListener("input", function () {
        var term = input.value.trim().toLowerCase();
        for (var j = 0; j < rows.length; j++) {
          var text = rows[j].getAttribute("data-filter-text") || "";
          rows[j].hidden = term.length > 0 && text.indexOf(term) === -1;
        }
      });
    })(inputs[i]);
  }
})();
