/* Reading controls: page jump, keyboard paging and remembered display mode.
   The server still renders every page, so this is only convenience. */
(function () {
  "use strict";

  var body = document.getElementById("reader-text");
  if (!body) { return; }

  var jump = document.querySelector("[data-reader-jump]");
  if (jump) {
    jump.addEventListener("change", function () {
      if (jump.form) { jump.form.submit(); }
    });
  }

  function setFont(size) {
    body.classList.remove("font-small", "font-normal", "font-large");
    body.classList.add("font-" + size);
    try { localStorage.setItem("rid-reader-font", size); } catch (err) {}
  }

  function setTheme(theme) {
    body.classList.remove("theme-paper", "theme-sepia", "theme-dark");
    body.classList.add("theme-" + theme);
    try { localStorage.setItem("rid-reader-theme", theme); } catch (err) {}
  }

  try { setFont(localStorage.getItem("rid-reader-font") || "normal"); } catch (err) { setFont("normal"); }
  try { setTheme(localStorage.getItem("rid-reader-theme") || "paper"); } catch (err) { setTheme("paper"); }

  Array.prototype.forEach.call(document.querySelectorAll("[data-reader-font]"), function (button) {
    button.addEventListener("click", function () { setFont(button.getAttribute("data-reader-font")); });
  });
  Array.prototype.forEach.call(document.querySelectorAll("[data-reader-theme]"), function (button) {
    button.addEventListener("click", function () { setTheme(button.getAttribute("data-reader-theme")); });
  });

  document.addEventListener("keydown", function (event) {
    var tag = (event.target && event.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") { return; }
    var link = null;
    if (event.key === "ArrowLeft") {
      link = document.querySelector(".reader-nav a[href*='page=']");
      var prev = document.querySelector(".reader-bottom-nav a[href*='page=']");
      if (prev && prev.textContent.indexOf("PREVIOUS") !== -1) { link = prev; }
    } else if (event.key === "ArrowRight") {
      var links = document.querySelectorAll(".reader-bottom-nav a[href*='page=']");
      for (var i = 0; i < links.length; i++) {
        if (links[i].textContent.indexOf("NEXT") !== -1) { link = links[i]; break; }
      }
      if (!link) {
        links = document.querySelectorAll(".reader-nav a[href*='page=']");
        for (var j = 0; j < links.length; j++) {
          if (links[j].textContent.indexOf("NEXT") !== -1) { link = links[j]; break; }
        }
      }
    }
    if (link) { event.preventDefault(); window.location.href = link.getAttribute("href"); }
  });
})();
