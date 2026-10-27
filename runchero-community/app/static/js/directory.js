document.querySelectorAll(".dir-entry").forEach(function (entry) {
  entry.addEventListener("toggle", function () {
    if (entry.open) {
      entry.setAttribute("aria-expanded", "true");
    } else {
      entry.removeAttribute("aria-expanded");
    }
  });
});
