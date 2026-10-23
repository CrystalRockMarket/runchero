/* Formula-shelf quick calculators.
   The expression is generated and checked by the seeder-side calculator
   builder. Inputs are numeric; the result is always shown with a
   double-check warning. */
(function () {
  "use strict";

  function show(container, message) {
    var out = container.querySelector("[data-calc-out]");
    if (out) { out.textContent = message; }
  }

  function calculate(container) {
    var expr = container.getAttribute("data-calc-expr") || "";
    var vars, labels;
    try {
      vars = JSON.parse(container.getAttribute("data-calc-vars") || "[]");
      labels = JSON.parse(container.getAttribute("data-calc-labels") || "{}");
    } catch (err) {
      show(container, "Calculator setup is unreadable.");
      return;
    }
    var values = {};
    var inputs = container.querySelectorAll("[data-calc-var]");
    for (var i = 0; i < inputs.length; i++) {
      var name = inputs[i].getAttribute("data-calc-var");
      var raw = inputs[i].value.trim();
      var value = Number(raw);
      if (raw === "" || !isFinite(value)) {
        show(container, "Fill in " + name + " (" + (labels[name] || name) + ").");
        inputs[i].focus();
        return;
      }
      values[name] = value;
    }
    var params = vars.map(function (_name, index) { return "v" + index; }).join(",");
    var args = vars.map(function (name) { return values[name]; });
    var result;
    try {
      var fn = new Function(params, "return (" + expr + ");");
      result = fn.apply(null, args);
    } catch (err) {
      show(container, "Could not evaluate this formula. Use the worked example.");
      return;
    }
    if (typeof result !== "number" || !isFinite(result)) {
      show(container, "That combination gives no finite result. Check units and zero values.");
      return;
    }
    var shown = Number(result.toPrecision(8)).toString();
    show(container, "RESULT: " + shown + "  (check it before use)");
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-calc]"), function (container) {
    var button = container.querySelector("[data-calc-run]");
    if (button) {
      button.addEventListener("click", function () { calculate(container); });
    }
    Array.prototype.forEach.call(container.querySelectorAll("[data-calc-var]"), function (input) {
      input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") { event.preventDefault(); calculate(container); }
      });
    });
  });
})();
