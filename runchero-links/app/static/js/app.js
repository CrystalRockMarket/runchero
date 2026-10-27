(function () {
  "use strict";

  var toast = document.getElementById("toast");
  var toastTimer = null;

  function announce(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("is-visible");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.classList.remove("is-visible");
    }, 2600);
  }

  function fallbackCopy(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (err) {
      ok = false;
    }
    document.body.removeChild(area);
    return ok;
  }

  function copyText(text) {
    if (!text) {
      announce("Nothing to copy yet.");
      return Promise.resolve(false);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(function () {
        announce("Copied to clipboard.");
        return true;
      }).catch(function () {
        if (fallbackCopy(text)) {
          announce("Copied to clipboard.");
          return true;
        }
        announce("Could not copy. Select the link and copy it by hand.");
        return false;
      });
    }
    if (fallbackCopy(text)) {
      announce("Copied to clipboard.");
      return Promise.resolve(true);
    }
    announce("Could not copy. Select the link and copy it by hand.");
    return Promise.resolve(false);
  }

  document.addEventListener("click", function (event) {
    var copyButton = event.target.closest("[data-copy-target]");
    if (copyButton) {
      var selector = copyButton.getAttribute("data-copy-target");
      var field = selector ? document.querySelector(selector) : null;
      copyText(field ? field.value : "");
      return;
    }

    var copyAll = event.target.closest("[data-copy-all]");
    if (copyAll) {
      var fields = document.querySelectorAll(".result-url");
      var values = [];
      fields.forEach(function (field) {
        if (field.value) values.push(field.value);
      });
      copyText(values.join("\n"));
      return;
    }

    var chip = event.target.closest("[data-search]");
    if (chip) {
      var form = document.getElementById("search-form");
      var input = document.getElementById("search-q");
      if (form && input) {
        event.preventDefault();
        input.value = chip.getAttribute("data-search") || chip.textContent;
        updateSearchPreview();
        if (typeof form.requestSubmit === "function") {
          form.requestSubmit();
        } else {
          form.submit();
        }
      }
    }
  });

  var searchForm = document.getElementById("search-form");
  var searchInput = document.getElementById("search-q");
  var searchPreview = document.getElementById("search-preview");

  function buildSearchUrl(keywords) {
    if (!searchForm) return "";
    var tagField = searchForm.querySelector('input[name="tag"]');
    var tag = tagField ? tagField.value : "";
    var base = searchForm.getAttribute("action") || "https://www.amazon.com/s";
    var query = "k=" + encodeURIComponent(keywords);
    if (tag) query += "&tag=" + encodeURIComponent(tag);
    return base + "?" + query;
  }

  function updateSearchPreview() {
    if (!searchInput || !searchPreview) return;
    var keywords = searchInput.value.trim();
    searchPreview.value = keywords ? buildSearchUrl(keywords) : "";
  }

  if (searchForm) {
    searchForm.addEventListener("submit", function () {
      updateSearchPreview();
    });
    if (searchInput) {
      searchInput.addEventListener("input", updateSearchPreview);
    }
    updateSearchPreview();
  }

  var totalInput = document.getElementById("order-total");
  var ordersInput = document.getElementById("orders-month");
  var rateInput = document.getElementById("commission-rate");
  var totalOut = document.getElementById("order-total-out");
  var ordersOut = document.getElementById("orders-month-out");
  var rateOut = document.getElementById("commission-rate-out");
  var perOrderOut = document.getElementById("per-order");
  var perMonthOut = document.getElementById("per-month");
  var perYearOut = document.getElementById("per-year");
  var exampleRate = document.getElementById("example-rate");
  var money = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });

  function rateLabel(rate) {
    return (Math.round(rate * 10) / 10).toString() + "%";
  }

  function updateEstimator() {
    if (!totalInput || !ordersInput || !rateInput) return;
    var total = parseFloat(totalInput.value) || 0;
    var orders = parseFloat(ordersInput.value) || 0;
    var rate = parseFloat(rateInput.value) || 0;
    var perOrder = total * rate / 100;
    var perMonth = perOrder * orders;
    var perYear = perMonth * 12;

    if (totalOut) totalOut.textContent = money.format(total).replace(".00", "");
    if (ordersOut) ordersOut.textContent = String(orders);
    if (rateOut) rateOut.textContent = rateLabel(rate);
    if (perOrderOut) perOrderOut.textContent = money.format(perOrder);
    if (perMonthOut) perMonthOut.textContent = money.format(perMonth);
    if (perYearOut) perYearOut.textContent = money.format(perYear);
    if (exampleRate) exampleRate.textContent = rateLabel(rate);

    document.querySelectorAll("[data-example-commission]").forEach(function (cell) {
      var price = parseFloat(cell.getAttribute("data-price")) || 0;
      cell.textContent = money.format(price * rate / 100);
    });
  }

  if (rateInput) {
    [totalInput, ordersInput, rateInput].forEach(function (input) {
      if (input) input.addEventListener("input", updateEstimator);
    });
    updateEstimator();
  }
})();
