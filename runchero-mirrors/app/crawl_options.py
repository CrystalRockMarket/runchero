"""Parse and resolve the optional advanced crawl settings."""
from __future__ import annotations

import json
from typing import Any

from . import config

OPTION_FIELDS = ("depth", "rate_kbps", "max_size_mb", "max_hours", "sockets")
SETTING_FIELDS = ("timeout", "retries", "robots", "scope", "keep_existing")

DEFAULT_SETTINGS: dict[str, Any] = {
    "timeout": 30,
    "retries": 2,
    "robots": 2,
    "scope": "address",
    "keep_existing": False,
}

LIMITS = {
    "depth": (1, 50),
    "rate_kbps": (1, 10_000),
    "max_size_mb": (1, 20_000),
    "max_hours": (0.25, 24),
    "sockets": (1, 8),
    "timeout": (5, 300),
    "retries": (0, 10),
}

FIELD_LABELS = {
    "depth": "Link depth",
    "rate_kbps": "Transfer rate",
    "max_size_mb": "Total size cap",
    "max_hours": "Time cap",
    "sockets": "Connections",
    "timeout": "Request timeout",
    "retries": "Retries",
}


def _number(raw: Any, *, integer: bool) -> int | float | None:
    text = str(raw or "").strip()
    if not text:
        return None
    try:
        value = int(text) if integer else float(text)
    except (TypeError, ValueError):
        return None
    return value


def parse_stored(raw: str | dict | None) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if isinstance(raw, str):
        try:
            raw = json.loads(raw) if raw.strip() else {}
        except (TypeError, ValueError):
            raw = {}
    if not isinstance(raw, dict):
        raw = {}

    overrides: dict[str, Any] = {}
    source = raw.get("overrides") if isinstance(raw.get("overrides"), dict) else {}
    for key in OPTION_FIELDS:
        integer = key != "max_hours"
        value = _number(source.get(key), integer=integer)
        if value is None:
            continue
        low, high = LIMITS[key]
        if low <= value <= high:
            overrides[key] = value

    settings = dict(DEFAULT_SETTINGS)
    for key in ("timeout", "retries"):
        value = _number(raw.get(key), integer=True)
        if value is not None and LIMITS[key][0] <= value <= LIMITS[key][1]:
            settings[key] = value
    if raw.get("robots") in (0, 2, "0", "2"):
        settings["robots"] = int(raw["robots"])
    if raw.get("scope") in ("address", "domain"):
        settings["scope"] = raw["scope"]
    if "keep_existing" in raw:
        settings["keep_existing"] = bool(raw["keep_existing"])
    return {"overrides": overrides, **settings}


def form_values(speed: str, raw: str | dict | None = None, *, rerun: bool = False) -> dict[str, str]:
    stored = parse_stored(raw)
    values = {
        "speed": speed,
        "timeout": str(stored["timeout"]),
        "retries": str(stored["retries"]),
        "robots": str(stored["robots"]),
        "scope": stored["scope"],
        "keep_existing": "1" if rerun else "",
    }
    for key in OPTION_FIELDS:
        value = stored["overrides"].get(key)
        values[key] = "" if value is None else str(value)
    return values


def parse_form(form: dict[str, str], *, rerun: bool = False) -> tuple[dict[str, Any], dict[str, str], dict[str, str]]:
    values = {
        "speed": (form.get("speed") or config.DEFAULT_SPEED).strip().lower(),
        "depth": (form.get("depth") or "").strip(),
        "rate_kbps": (form.get("rate_kbps") or "").strip(),
        "max_size_mb": (form.get("max_size_mb") or "").strip(),
        "max_hours": (form.get("max_hours") or "").strip(),
        "sockets": (form.get("sockets") or "").strip(),
        "timeout": (form.get("timeout") or str(DEFAULT_SETTINGS["timeout"])).strip(),
        "retries": (form.get("retries") or str(DEFAULT_SETTINGS["retries"])).strip(),
        "robots": (form.get("robots") or str(DEFAULT_SETTINGS["robots"])).strip(),
        "scope": (form.get("scope") or DEFAULT_SETTINGS["scope"]).strip(),
        "keep_existing": "1" if rerun and form.get("keep_existing") in ("1", "on", "true", "yes") else "",
    }
    errors: dict[str, str] = {}
    overrides: dict[str, Any] = {}

    for key in OPTION_FIELDS:
        text = values[key]
        if not text:
            continue
        integer = key != "max_hours"
        value = _number(text, integer=integer)
        if value is None:
            errors[key] = f"{FIELD_LABELS[key]} must be a number."
            continue
        low, high = LIMITS[key]
        if not low <= value <= high:
            if integer:
                errors[key] = f"Use a whole number from {int(low)} to {int(high)}."
            else:
                errors[key] = f"Use a number from {low:g} to {high:g}."
            continue
        overrides[key] = value

    settings = dict(DEFAULT_SETTINGS)
    for key in ("timeout", "retries"):
        value = _number(values[key], integer=True)
        if value is None or not LIMITS[key][0] <= value <= LIMITS[key][1]:
            low, high = LIMITS[key]
            errors[key] = f"Use a whole number from {low} to {high}."
        else:
            settings[key] = value

    if values["robots"] not in ("0", "2"):
        errors["robots"] = "Choose whether HTTrack should obey robots.txt."
    else:
        settings["robots"] = int(values["robots"])

    if values["scope"] not in ("address", "domain"):
        errors["scope"] = "Choose which part of the website should be copied."
    else:
        settings["scope"] = values["scope"]

    settings["keep_existing"] = bool(values["keep_existing"])
    if values["speed"] not in config.CRAWL_PROFILES:
        values["speed"] = config.DEFAULT_SPEED

    parsed = {"overrides": overrides, **settings}
    return parsed, values, errors


def resolve(speed: str, raw: str | dict | None = None) -> dict[str, Any]:
    stored = parse_stored(raw)
    base = config.profile(speed)
    overrides = stored["overrides"]
    return {
        "rate": int(round(float(overrides.get("rate_kbps", 0)) * 1000))
        if "rate_kbps" in overrides else int(base["rate"]),
        "depth": int(overrides.get("depth", base["depth"])),
        "sockets": int(overrides.get("sockets", base["sockets"])),
        "max_bytes": int(round(float(overrides.get("max_size_mb", 0)) * 1_000_000))
        if "max_size_mb" in overrides else int(base["max_bytes"]),
        "max_seconds": int(round(float(overrides["max_hours"]) * 3600))
        if "max_hours" in overrides else int(base["max_seconds"]),
        "timeout": stored["timeout"],
        "retries": stored["retries"],
        "robots": stored["robots"],
        "scope": stored["scope"],
        "keep_existing": stored["keep_existing"],
    }


def dump(options: dict[str, Any]) -> str:
    return json.dumps(options, separators=(",", ":"), sort_keys=True)


def summary(speed: str, raw: str | dict | None = None) -> dict[str, str]:
    options = resolve(speed, raw)
    return {
        "depth": str(options["depth"]),
        "rate": f"{max(1, round(options['rate'] / 1000))} KB/s",
        "sockets": str(options["sockets"]),
        "max_size": f"{options['max_bytes'] / 1_000_000:g} MB",
        "max_time": f"{options['max_seconds'] / 3600:g} h",
    }
