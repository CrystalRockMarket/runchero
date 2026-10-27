"""Validate, normalise, and display the ways a listing can be reached."""
from __future__ import annotations

import re
from urllib.parse import urlsplit

from . import config

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_ALLOWED = re.compile(r"^[0-9+()\-.\s]+$")


class ChannelError(ValueError):
    pass


def clean(value: str, limit: int) -> str:
    return (value or "").replace("\x00", "").strip()[:limit]


def normalise_url(value: str, base: str | None = None) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if len(text) > config.MAX_CHANNEL_VALUE:
        raise ChannelError("That link is too long.")
    if text.startswith("@"):
        text = text[1:]
    has_scheme = bool(re.match(r"^https?://", text, re.IGNORECASE))
    if base and not has_scheme:
        lowered = text.lower()
        if lowered.startswith(("www.facebook.com/", "facebook.com/",
                               "www.instagram.com/", "instagram.com/")):
            text = "https://" + text
        else:
            text = base.rstrip("/") + "/" + text.lstrip("/")
    elif not has_scheme:
        if " " in text or "." not in text:
            raise ChannelError("Links need to start with https://")
        text = "https://" + text
    parts = urlsplit(text)
    if parts.scheme.lower() not in ("http", "https"):
        raise ChannelError("Only http and https links are allowed.")
    if not parts.hostname or "." not in parts.hostname:
        raise ChannelError("That link is missing a valid website address.")
    if parts.username or parts.password:
        raise ChannelError("Links with a username or password are not allowed.")
    return text


def normalise_email(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if len(text) > config.MAX_CHANNEL_VALUE or not EMAIL_RE.match(text):
        raise ChannelError("That email address does not look valid.")
    return text


def normalise_phone(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if len(text) > config.MAX_CHANNEL_VALUE or not PHONE_ALLOWED.match(text):
        raise ChannelError("Phone numbers can only use digits, spaces, +, -, ( and ).")
    digits = re.sub(r"\D", "", text)
    if len(digits) < 7:
        raise ChannelError("That phone number looks too short.")
    return text


def _contact(label: str, value: str, sort: int, normaliser) -> dict | None:
    text = normaliser(value)
    if not text:
        return None
    return {"kind": "contact", "label": label, "value": text, "sort_order": sort}


def parse_channels(form: dict[str, str]) -> tuple[list[dict], list[str]]:
    channels: list[dict] = []
    errors: list[str] = []

    def add(label: str, field: str, normaliser, sort: int) -> None:
        try:
            channel = _contact(label, form.get(field, ""), sort, normaliser)
        except ChannelError as exc:
            errors.append(f"{label}: {exc}")
            return
        if channel:
            channels.append(channel)

    add("Phone", "phone", normalise_phone, 10)
    add("Email", "email", normalise_email, 20)

    for label, field, base, sort in (
        ("Facebook", "facebook", "https://www.facebook.com", 30),
        ("Instagram", "instagram", "https://www.instagram.com", 40),
        ("Website", "website", None, 50),
    ):
        try:
            url = normalise_url(form.get(field, ""), base=base)
        except ChannelError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if url:
            channels.append({"kind": "link", "label": label, "value": url,
                             "sort_order": sort})

    add("Address", "address", lambda value: clean(value, config.MAX_CHANNEL_VALUE), 60)

    for index in range(1, config.MAX_CUSTOM + 1):
        label = clean(form.get(f"custom_label_{index}", ""), config.MAX_CHANNEL_LABEL)
        raw = clean(form.get(f"custom_value_{index}", ""), config.MAX_CHANNEL_VALUE)
        if not raw:
            continue
        is_link = bool(re.match(r"^https?://", raw, re.IGNORECASE))
        if is_link:
            try:
                value = normalise_url(raw)
            except ChannelError as exc:
                errors.append(f"{label or 'Link'}: {exc}")
                continue
            channels.append({
                "kind": "link",
                "label": label or "Link",
                "value": value,
                "sort_order": 70 + index,
            })
        else:
            channels.append({
                "kind": "contact",
                "label": label or "Contact",
                "value": raw,
                "sort_order": 70 + index,
            })

    return channels, errors


def channel_href(channel: dict) -> str:
    kind = channel.get("kind", "contact")
    label = (channel.get("label") or "").lower()
    value = channel.get("value") or ""
    if kind == "link" or re.match(r"^https?://", value, re.IGNORECASE):
        if re.match(r"^https?://", value, re.IGNORECASE):
            return value
        return ""
    if label == "email" or (EMAIL_RE.match(value) and "@" in value):
        return "mailto:" + value
    if label == "phone":
        digits = re.sub(r"[^\d+]", "", value)
        return "tel:" + digits if digits else ""
    if PHONE_ALLOWED.match(value) and len(re.sub(r"\D", "", value)) >= 7:
        return "tel:" + re.sub(r"[^\d+]", "", value)
    return ""


def decorate(channels: list[dict]) -> list[dict]:
    decorated = []
    for channel in channels:
        item = dict(channel)
        item["href"] = channel_href(item)
        item["external"] = item["href"].startswith("http")
        if item["kind"] == "link" and not item["href"]:
            item["kind"] = "contact"
        decorated.append(item)
    return decorated


def split_for_edit(channels: list[dict]) -> dict:
    known = {channel["label"]: channel for channel in channels if channel["kind"] != "custom"}
    fixed = {}
    custom = []
    for label, field in (
        ("Phone", "phone"),
        ("Email", "email"),
        ("Facebook", "facebook"),
        ("Instagram", "instagram"),
        ("Website", "website"),
        ("Address", "address"),
    ):
        fixed[field] = known.get(label, {}).get("value", "")
    for channel in channels:
        if channel["label"] in ("Phone", "Email", "Facebook", "Instagram",
                                "Website", "Address"):
            continue
        custom.append({"label": channel["label"], "value": channel["value"],
                       "kind": channel["kind"]})
    while len(custom) < config.MAX_CUSTOM:
        custom.append({"label": "", "value": "", "kind": "contact"})
    return {"fixed": fixed, "custom": custom[:config.MAX_CUSTOM]}
