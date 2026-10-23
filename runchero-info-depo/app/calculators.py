"""Small, deliberately conservative formula calculators.

The formula shelf contains prose formulas, multi-step recipes and equations
with several rearrangements. A calculator is only offered when the expression
is a single equation that can be evaluated safely from the symbols listed in
the record. Everything else stays a read-and-work-it-out formula.
"""
from __future__ import annotations

import math
import re
from typing import Any

FUNCTIONS = {
    "sqrt": "Math.sqrt",
    "sin": "Math.sin",
    "cos": "Math.cos",
    "tan": "Math.tan",
    "asin": "Math.asin",
    "acos": "Math.acos",
    "atan": "Math.atan",
    "atan2": "Math.atan2",
    "abs": "Math.abs",
    "exp": "Math.exp",
    "log": "Math.log",
    "ln": "Math.log",
}
CONSTANTS = {"pi": "Math.PI", "e": "Math.E"}


def _strip_rhs(expression: str) -> tuple[str, str] | None:
    text = expression.strip().splitlines()[0].strip()
    if text.count("=") < 1:
        return None
    left, right = text.split("=", 1)
    left = left.strip()
    if not left or any(ch in left for ch in "/()[]"):
        return None
    if any(op in left for op in ("+", "*", "^")) or " x " in left.lower():
        return None
    # Drop a second rearrangement such as "(so I = V / R...)" or
    # "(C = (F - 32) x 5 / 9)".
    right = re.split(r"\s{2,}\(", right, flags=re.I)[0]
    right = re.split(r"\s{2,}(?:for|where|so|with|if)\s+", right, flags=re.I)[0]
    right = re.sub(r"\s+\([^()]*=[^()]*\)\s*$", "", right).strip()
    right = right.split(";")[0].strip()
    if not right or "=" in right:
        return None
    if any(bad in right for bad in ("+/-", "d/dx", "integral", "|", "->",
                                     "square root of", "sum of", "root 3",
                                     "log10", "proportional", "constant")):
        return None
    if re.search(r"\d\s*\(", right):
        return None
    return left, right


def _symbol_vars(symbols: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for part in re.split(r"[;\n]", symbols or ""):
        match = re.match(r"\s*([A-Za-z_][A-Za-z0-9_,\s]*?)\s*=\s*(.*)", part)
        if not match:
            continue
        names = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", match.group(1))
        for name in names:
            if name not in FUNCTIONS and name not in CONSTANTS:
                found[name] = match.group(2).strip()
    return found


def _default_value(description: str) -> float | None:
    match = re.match(r"\s*(-?\d+(?:\.\d+)?)\s*(?:[A-Za-z%]|$)", description or "")
    if not match:
        return None
    try:
        value = float(match.group(1))
    except ValueError:
        return None
    return value if value >= 0 else None


def _normalise(right: str, symbols: dict[str, str]) -> tuple[str, list[str], dict[str, float]] | None:
    right = (right.replace("×", "*").replace("÷", "/").replace("−", "-")
                  .replace("²", "^2").replace("³", "^3"))
    if "%" in right or ":" in right:
        return None

    # Turn r2, A1, V0.16 into powers when the base is a known symbol. Do not
    # touch names that are themselves symbols (x1 may be a variable).
    def power(match: re.Match) -> str:
        base = match.group(1)
        return f"{base}^{match.group(2)}"

    names = sorted(symbols, key=len, reverse=True)
    if names:
        pattern = re.compile(r"\b(" + "|".join(re.escape(n) for n in names) +
                             r")(\d+(?:\.\d+)?)")
        # Skip a base if the longer name including the digits is itself a symbol.
        def power_guard(match: re.Match) -> str:
            whole = match.group(1) + match.group(2)
            if whole in symbols:
                return whole
            return f"{match.group(1)}^{match.group(2)}"
        right = pattern.sub(power_guard, right)

    token_re = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|\.\d+|[()+\-*/^,]")
    tokens = token_re.findall(right)
    if not tokens:
        return None
    rendered: list[str] = []
    used: list[str] = []
    prev_kind = ""

    def var_ref(name: str) -> str:
        if name not in used:
            used.append(name)
        return f"v{used.index(name)}"
    for token in tokens:
        if re.match(r"^[A-Za-z_]", token):
            if token in FUNCTIONS:
                rendered.append(FUNCTIONS[token])
                prev_kind = "func"
            elif token in CONSTANTS:
                rendered.append(CONSTANTS[token])
                prev_kind = "value"
            elif token in symbols:
                rendered.append(var_ref(token))
                prev_kind = "value"
            elif token == "x" and "x" not in symbols:
                rendered.append("*")
                prev_kind = "op"
            elif len(token) == 1 and token != "x":
                # A one-letter input used by the equation but not described in
                # the symbol list. This covers terse formulas such as a, b, c.
                symbols[token] = token
                rendered.append(var_ref(token))
                prev_kind = "value"
            else:
                # A power such as r^2 is already expanded; any other identifier
                # is prose or a missing symbol, so do not guess.
                return None
        elif re.match(r"^(\d|\.)", token):
            rendered.append(token)
            prev_kind = "value"
        elif token == "(":
            if prev_kind == "value":
                rendered.append("*")
            rendered.append("(")
            prev_kind = "open"
        elif token == ")":
            rendered.append(")")
            prev_kind = "value"
        else:
            rendered.append(token)
            prev_kind = "op" if token in "+-*/^" else ""
    expr = "".join(rendered)
    expr = re.sub(r"(?<=[0-9)])(?=[A-Za-z(])", "*", expr)
    expr = expr.replace("^", "**")
    if not used:
        return None
    if re.search(r"[^0-9A-Za-z_+\-*/().,Math\s]", expr):
        return None
    if "*(*" in expr or expr.count("(") != expr.count(")"):
        return None
    defaults = {name: _default_value(symbols[name]) for name in used}
    return expr, used, {k: v for k, v in defaults.items() if v is not None}


def _sample(expr: str, used: list[str], defaults: dict[str, float],
            offset: float) -> float | None:
    env = {f"v{index}": defaults.get(name, 2.4 + index * 0.7 + offset)
           for index, name in enumerate(used)}
    py_expr = (expr.replace("Math.PI", "math.pi").replace("Math.E", "math.e")
                   .replace("Math.", "math."))
    try:
        value = eval(py_expr, {"math": math}, env)  # noqa: S307 - generated, checked
    except Exception:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def calculator_for(expression: str, symbols: str) -> dict[str, Any] | None:
    stripped = _strip_rhs(expression)
    if not stripped:
        return None
    left, right = stripped
    symbol_map = _symbol_vars(symbols)
    normalised = _normalise(right, symbol_map)
    if not normalised:
        return None
    expr, used, defaults = normalised
    if not used or len(used) > 8:
        return None
    if not any(_sample(expr, used, defaults, offset) is not None
               for offset in (0.0, 1.7, 5.0)):
        return None
    labels = {}
    for name in used:
        description = symbol_map.get(name, "")
        labels[name] = description or name
    return {
        "label": left,
        "expr": expr,
        "vars": used,
        "labels": labels,
        "defaults": defaults,
    }
