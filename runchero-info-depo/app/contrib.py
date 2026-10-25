"""Public change requests and the review actions that apply them.

The public can suggest a new brand, equipment type, model, category, collection
or source. Nothing enters the catalogue until an administrator approves it.
Requests are stored as a small JSON payload plus review metadata, which keeps
the schema stable as request types evolve.
"""
from __future__ import annotations

import json
import re
import sqlite3
import threading
import time
from collections import defaultdict, deque
from typing import Any
from urllib.parse import quote_plus

from . import equipment
from .seed.collections import (ANIMAL_GROUPS, CROP_GROUPS, GROUP_TITLES,
                               TOPIC_GROUPS)

ICONS = [
    "archive", "book", "bolt", "calendar", "carrot", "chat", "check", "chicken",
    "clock", "corn", "cow", "depot", "dog", "download", "droplet", "egg",
    "engine", "fence", "fire", "firstaid", "gearbox", "grass", "hay", "home",
    "info", "jar", "list", "magnifier", "meat", "milk", "notes", "potato",
    "saw", "seedling", "shield", "star", "sun", "tag", "tomato", "tool",
    "tractor", "tree", "truck", "weld", "wheat", "wrench",
]
ACCENTS = ["grass", "grass2", "grass3", "sun", "sun2", "tomato", "tomato2",
           "orange", "brown", "teal", "teal2", "plum", "pink", "cyan", "sky",
           "sky2"]
CATEGORY_KINDS = [
    ("library", "Library shelf"),
    ("article", "Article section"),
]
COLLECTION_KINDS = [("crop", "Crop"), ("animal", "Animal"), ("topic", "Topic")]
SOURCE_KINDS = [
    ("book", "Public-domain book"),
    ("manual", "Factory or service manual"),
    ("archive", "Archive collection"),
    ("dataset", "Dataset"),
    ("website", "Website"),
    ("forum", "Forum thread"),
    ("other", "Other"),
]
REQUEST_KIND_LABELS = {
    "brand": "New brand",
    "equipment-type": "New equipment type",
    "model": "New model record",
    "category": "New category",
    "collection": "New collection shelf",
    "source": "New source",
    "other": "Something else",
}


def slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower())
    return value.strip("-")[:80]


def _option(value: str, label: str) -> dict[str, str]:
    return {"value": value, "label": label}


def equipment_options(conn) -> list[dict[str, str]]:
    kinds, _groups = equipment.merged_taxonomy(conn)
    return [_option(slug, meta["label"])
            for slug, meta in sorted(kinds.items(),
                                     key=lambda pair: pair[1]["label"].lower())]


def group_options(conn) -> list[dict[str, str]]:
    _kinds, groups = equipment.merged_taxonomy(conn)
    return [_option(group["slug"], group["name"]) for group in groups]


def collection_group_options() -> list[dict[str, str]]:
    options = []
    for group_slug, name in {**CROP_GROUPS, **ANIMAL_GROUPS,
                             **TOPIC_GROUPS}.items():
        options.append(_option(group_slug, name))
    return options


def field_specs(conn, kind: str) -> list[dict[str, Any]]:
    """Plain form metadata shared by the public form and admin editor."""
    if kind == "brand":
        return [
            {"name": "kind", "label": "Equipment type", "type": "select",
             "options": equipment_options(conn), "required": True},
            {"name": "name", "label": "Brand or make", "type": "text",
             "required": True, "maxlength": 80,
             "placeholder": "e.g. County, Aebi, Wadkin"},
            {"name": "url", "label": "Reference link", "type": "url",
             "placeholder": "https://..."},
            {"name": "notes", "label": "Evidence or notes", "type": "textarea",
             "placeholder": "Where did you see this brand? Which machines?"},
        ]
    if kind == "equipment-type":
        return [
            {"name": "group_slug", "label": "Group", "type": "select",
             "options": group_options(conn), "required": True},
            {"name": "label", "label": "Type name", "type": "text",
             "required": True, "maxlength": 80,
             "placeholder": "e.g. Sugar beet harvesters"},
            {"name": "slug", "label": "URL slug (optional)", "type": "text",
             "maxlength": 60, "placeholder": "auto-generated if blank"},
            {"name": "icon", "label": "Icon", "type": "select",
             "options": [_option(i, i.replace("-", " ").title()) for i in ICONS],
             "default": "tool"},
            {"name": "description", "label": "Short description", "type": "textarea",
             "required": True, "maxlength": 500},
        ]
    if kind == "model":
        return [
            {"name": "kind", "label": "Equipment type", "type": "select",
             "options": equipment_options(conn), "required": True},
            {"name": "make", "label": "Make / brand", "type": "text",
             "required": True, "maxlength": 80},
            {"name": "model", "label": "Model", "type": "text",
             "required": True, "maxlength": 120},
            {"name": "year_from", "label": "Year from", "type": "number",
             "min": 1800, "max": 2100},
            {"name": "year_to", "label": "Year to", "type": "number",
             "min": 1800, "max": 2100},
            {"name": "engine", "label": "Engine", "type": "text", "maxlength": 120},
            {"name": "drive", "label": "Drive / transmission", "type": "text",
             "maxlength": 120},
            {"name": "power", "label": "Power", "type": "text", "maxlength": 80},
            {"name": "notes", "label": "Specifications and notes", "type": "textarea",
             "maxlength": 2000},
            {"name": "url", "label": "Reference link", "type": "url"},
        ]
    if kind == "category":
        return [
            {"name": "name", "label": "Category name", "type": "text",
             "required": True, "maxlength": 80},
            {"name": "slug", "label": "URL slug (optional)", "type": "text",
             "maxlength": 60, "placeholder": "auto-generated if blank"},
            {"name": "kind", "label": "Shelf type", "type": "select",
             "options": [_option(v, l) for v, l in CATEGORY_KINDS],
             "default": "library"},
            {"name": "icon", "label": "Icon", "type": "select",
             "options": [_option(i, i.replace("-", " ").title()) for i in ICONS],
             "default": "list"},
            {"name": "accent", "label": "Accent colour", "type": "select",
             "options": [_option(i, i.title()) for i in ACCENTS],
             "default": "grass"},
            {"name": "blurb", "label": "What belongs here?", "type": "textarea",
             "maxlength": 500},
        ]
    if kind == "collection":
        return [
            {"name": "name", "label": "Shelf name", "type": "text",
             "required": True, "maxlength": 80,
             "placeholder": "e.g. Quinoa, Working donkeys, Beekeeping"},
            {"name": "slug", "label": "URL slug (optional)", "type": "text",
             "maxlength": 60, "placeholder": "auto-generated if blank"},
            {"name": "kind", "label": "Collection kind", "type": "select",
             "options": [_option(v, l) for v, l in COLLECTION_KINDS],
             "default": "crop"},
            {"name": "group_slug", "label": "Group", "type": "select",
             "options": collection_group_options(), "required": True},
            {"name": "subgroup", "label": "Subgroup slug (optional)", "type": "text",
             "maxlength": 60, "placeholder": "e.g. overview"},
            {"name": "summary", "label": "Scope note", "type": "textarea",
             "maxlength": 500},
            {"name": "aliases", "label": "Aliases", "type": "text", "maxlength": 160},
            {"name": "icon", "label": "Icon", "type": "select",
             "options": [_option(i, i.replace("-", " ").title()) for i in ICONS],
             "default": "seedling"},
            {"name": "accent", "label": "Accent colour", "type": "select",
             "options": [_option(i, i.title()) for i in ACCENTS],
             "default": "grass"},
        ]
    if kind == "source":
        return [
            {"name": "title", "label": "Source title", "type": "text",
             "required": True, "maxlength": 200},
            {"name": "author", "label": "Author or publisher", "type": "text",
             "maxlength": 120},
            {"name": "source_kind", "label": "Source type", "type": "select",
             "options": [_option(v, l) for v, l in SOURCE_KINDS],
             "default": "book"},
            {"name": "url", "label": "Download or landing-page URL", "type": "url",
             "required": True},
            {"name": "license", "label": "Licence", "type": "text", "maxlength": 120,
             "placeholder": "e.g. Public domain, CC0, CC BY 4.0"},
            {"name": "note", "label": "Why is it useful?", "type": "textarea",
             "maxlength": 800},
        ]
    if kind == "other":
        return [
            {"name": "title", "label": "Short title", "type": "text",
             "required": True, "maxlength": 120},
            {"name": "details", "label": "What should be added or fixed?",
             "type": "textarea", "required": True, "maxlength": 4000},
            {"name": "url", "label": "Supporting link", "type": "url"},
        ]
    raise ValueError("unknown request kind")


def parse_request(conn, kind: str, form: dict) -> tuple[dict[str, Any], dict[str, str]]:
    payload: dict[str, Any] = {}
    errors: dict[str, str] = {}
    for field in field_specs(conn, kind):
        name = field["name"]
        raw = form.get(name, "")
        if isinstance(raw, list):
            raw = raw[-1] if raw else ""
        raw = (raw or "").strip()
        if field.get("required") and not raw:
            errors[name] = "This field is required."
            continue
        if not raw:
            payload[name] = "" if field["type"] != "number" else None
            continue
        maxlength = field.get("maxlength")
        if maxlength and len(raw) > maxlength:
            errors[name] = f"Keep this under {maxlength} characters."
            continue
        if field["type"] == "number":
            try:
                number = int(raw)
            except ValueError:
                errors[name] = "Enter a whole year."
                continue
            if "min" in field and number < field["min"]:
                errors[name] = f"Must be {field['min']} or later."
                continue
            if "max" in field and number > field["max"]:
                errors[name] = f"Must be {field['max']} or earlier."
                continue
            payload[name] = number
            continue
        if field["type"] == "select":
            allowed = {option["value"] for option in field["options"]}
            if raw not in allowed:
                errors[name] = "Choose one of the listed options."
                continue
            payload[name] = raw
            continue
        if field["type"] == "url":
            if not re.match(r"^https?://[^\s]+$", raw, re.I):
                errors[name] = "Use a full http:// or https:// link."
                continue
        payload[name] = raw

    if errors:
        return payload, errors

    kinds, groups = equipment.merged_taxonomy(conn)
    if kind == "brand":
        slug = payload["kind"]
        if slug not in kinds:
            errors["kind"] = "Unknown equipment type."
        else:
            wanted = payload["name"].casefold()
            if any(brand.casefold() == wanted for brand in kinds[slug]["brands"]):
                errors["name"] = ("That brand is already in this equipment "
                                  "menu. Submit a correction instead.")
    elif kind == "equipment-type":
        if payload["group_slug"] not in {group["slug"] for group in groups}:
            errors["group_slug"] = "Unknown equipment group."
        slug = slugify(payload.get("slug") or payload["label"])
        if not slug:
            errors["slug"] = "Could not make a URL slug from that name."
        elif slug in kinds:
            errors["slug"] = "That type slug is already in use."
        else:
            payload["slug"] = slug
        payload["icon"] = payload.get("icon") or "tool"
    elif kind == "model":
        if payload["kind"] not in kinds:
            errors["kind"] = "Unknown equipment type."
        duplicate = conn.execute(
            "SELECT id FROM vehicles WHERE kind=? AND "
            "LOWER(make)=LOWER(?) AND LOWER(model)=LOWER(?)",
            (payload["kind"], payload["make"], payload["model"])).fetchone()
        if duplicate:
            errors["model"] = "That model record already exists."
    elif kind == "category":
        slug = slugify(payload.get("slug") or payload["name"])
        if not slug:
            errors["slug"] = "Could not make a URL slug from that name."
        elif conn.execute("SELECT 1 FROM categories WHERE slug=?", (slug,)).fetchone():
            errors["slug"] = "That category slug is already in use."
        else:
            payload["slug"] = slug
        payload["icon"] = payload.get("icon") or "list"
        payload["accent"] = payload.get("accent") or "grass"
    elif kind == "collection":
        slug = slugify(payload.get("slug") or payload["name"])
        if not slug:
            errors["slug"] = "Could not make a URL slug from that name."
        elif conn.execute("SELECT 1 FROM collections WHERE slug=?", (slug,)).fetchone():
            errors["slug"] = "That collection slug is already in use."
        else:
            payload["slug"] = slug
        group = payload.get("group_slug")
        if group not in GROUP_TITLES:
            errors["group_slug"] = "Unknown collection group."
        expected = {"crop": CROP_GROUPS, "animal": ANIMAL_GROUPS,
                    "topic": TOPIC_GROUPS}.get(payload["kind"], {})
        if group in GROUP_TITLES and group not in expected:
            errors["group_slug"] = "That group does not belong to this collection kind."
        payload["subgroup"] = slugify(payload.get("subgroup") or "overview")
        payload["icon"] = payload.get("icon") or "seedling"
        payload["accent"] = payload.get("accent") or "grass"
    elif kind == "source":
        if conn.execute("SELECT 1 FROM sources WHERE url=?", (payload["url"],)).fetchone():
            errors["url"] = "That source URL is already listed."
    return payload, errors


def title_for(conn, kind: str, payload: dict) -> str:
    if kind == "brand":
        kinds, _ = equipment.merged_taxonomy(conn)
        return f"{payload.get('name', '')} - {kinds.get(payload.get('kind'), {}).get('label', 'equipment')}"
    if kind == "equipment-type":
        return payload.get("label", "Equipment type")
    if kind == "model":
        return f"{payload.get('make', '')} {payload.get('model', '')}".strip()
    if kind == "category":
        return payload.get("name", "Category")
    if kind == "collection":
        return payload.get("name", "Collection")
    if kind == "source":
        return payload.get("title", "Source")
    return payload.get("title", "Request")


def create_request(conn, kind: str, payload: dict, contact: str = "",
                   ip: str = "") -> int:
    title = title_for(conn, kind, payload)
    cur = conn.execute(
        "INSERT INTO change_requests(kind, title, payload, contact, ip) "
        "VALUES(?,?,?,?,?)",
        (kind, title, json.dumps(payload, ensure_ascii=False), contact[:160], ip[:64]),
    )
    conn.commit()
    return int(cur.lastrowid)


def update_payload(conn, request_id: int, kind: str, payload: dict) -> None:
    conn.execute(
        "UPDATE change_requests SET kind=?, title=?, payload=? WHERE id=?",
        (kind, title_for(conn, kind, payload),
         json.dumps(payload, ensure_ascii=False), request_id),
    )


def _unique_slug(conn, table: str, base: str) -> str:
    slug = slugify(base) or "item"
    candidate = slug
    n = 2
    while conn.execute(f"SELECT 1 FROM {table} WHERE slug=?", (candidate,)).fetchone():
        candidate = f"{slug}-{n}"
        n += 1
    return candidate


def apply_request(conn, request_id: int, kind: str,
                  payload: dict) -> tuple[bool, str, str]:
    """Insert the approved record. Returns (ok, message, public URL)."""
    try:
        if kind == "brand":
            conn.execute(
                "INSERT INTO equipment_brands(kind, name, url, note, request_id) "
                "VALUES(?,?,?,?,?)",
                (payload["kind"], payload["name"], payload.get("url", ""),
                 payload.get("notes", ""), request_id),
            )
            return True, "Brand added to the coverage menu.", (
                f"/repair?type={payload['kind']}&make="
                f"{quote_plus(payload['name'])}")
        if kind == "equipment-type":
            conn.execute(
                "INSERT INTO equipment_types(slug, label, group_slug, icon, "
                "description, request_id) VALUES(?,?,?,?,?,?)",
                (payload["slug"], payload["label"], payload["group_slug"],
                 payload.get("icon", "tool"), payload.get("description", ""),
                 request_id),
            )
            return True, "Equipment type added to Repair.", (
                f"/repair?type={payload['slug']}")
        if kind == "model":
            slug = _unique_slug(conn, "vehicles",
                                f"{payload['make']}-{payload['model']}")
            notes = payload.get("notes", "")
            if payload.get("url"):
                notes = f"{notes}\nReference: {payload['url']}".strip()
            conn.execute(
                "INSERT INTO vehicles(slug, kind, make, model, year_from, year_to, "
                "engine, drive, power, notes, origin) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (slug, payload["kind"], payload["make"], payload["model"],
                 payload.get("year_from") or None, payload.get("year_to") or None,
                 payload.get("engine", ""), payload.get("drive", ""),
                 payload.get("power", ""), notes, "community"),
            )
            return True, "Model record added.", f"/vehicles/{slug}"
        if kind == "category":
            order = conn.execute(
                "SELECT COALESCE(MAX(sort_order), 0) + 1 FROM categories").fetchone()[0]
            conn.execute(
                "INSERT INTO categories(slug, name, icon, accent, blurb, kind, "
                "sort_order) VALUES(?,?,?,?,?,?,?)",
                (payload["slug"], payload["name"], payload.get("icon", "list"),
                 payload.get("accent", "grass"), payload.get("blurb", ""),
                 payload.get("kind", "library"), order),
            )
            ref = (f"/library/archive?cat={payload['slug']}"
                   if payload.get("kind") == "library"
                   else f"/section/{payload['slug']}")
            return True, "Category created.", ref
        if kind == "collection":
            order = conn.execute(
                "SELECT COALESCE(MAX(sort_order), 0) + 1 FROM collections").fetchone()[0]
            group = payload["group_slug"]
            conn.execute(
                "INSERT INTO collections(slug, name, kind, group_slug, group_name, "
                "subgroup_slug, subgroup_name, icon, accent, summary, aliases, "
                "sort_order) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (payload["slug"], payload["name"], payload["kind"], group,
                 GROUP_TITLES[group], payload["subgroup"],
                 payload["subgroup"].replace("-", " ").title(),
                 payload.get("icon", "seedling"), payload.get("accent", "grass"),
                 payload.get("summary", ""), payload.get("aliases", ""), order),
            )
            prefix = {"crop": "/grow", "animal": "/animals",
                      "topic": "/topic"}[payload["kind"]]
            return True, "Collection shelf created.", f"{prefix}/{payload['slug']}"
        if kind == "source":
            slug = _unique_slug(conn, "sources", payload["title"])
            conn.execute(
                "INSERT INTO sources(slug, title, author, kind, url, license, note) "
                "VALUES(?,?,?,?,?,?,?)",
                (slug, payload["title"], payload.get("author", ""),
                 payload.get("source_kind", "other"), payload["url"],
                 payload.get("license", ""), payload.get("note", "")),
            )
            return True, "Source added.", "/sources?q=" + slug
        return True, "Request approved. No catalogue row was needed.", ""
    except sqlite3.IntegrityError as exc:
        return False, f"The catalogue rejected this record: {exc}.", ""


def status_counts(conn) -> dict[str, int]:
    result = {row["status"]: row["n"] for row in conn.execute(
        "SELECT status, COUNT(*) n FROM change_requests GROUP BY status")}
    result["total"] = sum(result.values())
    return result


# Simple in-process abuse guard. Good enough for a single depot; restarts clear it.
_RATE_LOCK = threading.Lock()
_RATE: dict[str, deque[float]] = defaultdict(deque)


def rate_ok(key: str, limit: int = 6, window: int = 600) -> bool:
    now = time.monotonic()
    with _RATE_LOCK:
        bucket = _RATE[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True
