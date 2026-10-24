"""Guided add-site walkthrough and mirror controls."""
from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, urlunparse

from .. import config, db
from ..services import httrack
from ..web import render
from . import flash, page_context, redirect

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def register(add):
    add("GET", re.compile(r"^/add$"), walkthrough)
    add("POST", re.compile(r"^/add$"), add_submit)
    add("POST", re.compile(r"^/start/(?P<id>\d+)$"), start_job)
    add("POST", re.compile(r"^/pause/(?P<id>\d+)$"), pause_job)
    add("POST", re.compile(r"^/resume/(?P<id>\d+)$"), resume_job)
    add("POST", re.compile(r"^/stop/(?P<id>\d+)$"), stop_job)
    add("POST", re.compile(r"^/retry/(?P<id>\d+)$"), retry_job)
    add("GET", re.compile(r"^/logs/(?P<id>\d+)$"), view_log)


def _slugify(name: str) -> str:
    value = _SLUG_RE.sub("-", (name or "").lower()).strip("-")
    return (value or "site")[:80].strip("-") or "site"


def _is_private_host(host: str) -> bool:
    raw = (host or "").strip("[]").lower()
    if raw in {"localhost", "localhost.localdomain"} or raw.endswith(".local"):
        return True
    try:
        address = ipaddress.ip_address(raw)
        return not address.is_global
    except ValueError:
        return False


def _validate_url(raw: str) -> tuple[str | None, str | None]:
    value = (raw or "").strip()
    if not value:
        return None, "Please enter the website address you want to save."
    if len(value) > 2000:
        return None, "That address is too long."
    if any(ch in value for ch in ("\n", "\r", "\t", " ")):
        return None, "The address cannot contain spaces."
    if not value.lower().startswith(("http://", "https://")):
        return None, "Please start the address with http:// or https://."
    try:
        parsed = urlparse(value)
    except ValueError:
        return None, "That does not look like a valid web address."
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        return None, "That does not look like a valid web address."
    if parsed.username or parsed.password:
        return None, "Please remove any username or password from the address."
    host = parsed.hostname or ""
    if not host:
        return None, "That address is missing a website name."
    try:
        port = parsed.port
    except ValueError:
        return None, "That website port is not valid."
    if not config.ALLOW_PRIVATE_HOSTS and _is_private_host(host):
        return None, "That address points to a private or local network location. Please use a public website."
    scheme = parsed.scheme.lower()
    netloc = f"[{host.lower()}]" if ":" in host else host.lower()
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc += f":{port}"
    path = parsed.path or "/"
    normalized = urlunparse((scheme, netloc, path, "", parsed.query, ""))
    return normalized, None


def _duplicate(conn, normalized: str, raw: str):
    def key(value: str) -> str:
        try:
            p = urlparse(value)
            path = (p.path or "/").rstrip("/") or "/"
            if not p.hostname:
                return value.lower()
            host = p.hostname.lower()
            try:
                port = p.port
            except ValueError:
                port = None
            if port:
                host += f":{port}"
            return f"{host}{path}?{p.query}"
        except Exception:
            return value.lower()

    wanted = key(normalized)
    rows = db.rows(
        conn,
        "SELECT id, name, slug, url, status FROM mirrors "
        "WHERE status IN ('queued','starting','running','paused','completed') "
        "ORDER BY id DESC",
    )
    for row in rows:
        if key(row["url"]) == wanted or key(raw) == wanted:
            return row
    return None


def _render_add(conn, req, *, errors=None, values=None, status=200, duplicate=None):
    values = values or {}
    ctx = page_context(
        conn,
        req,
        title="Add a site",
        errors=errors or {},
        values=values,
        duplicate=duplicate,
    )
    return status, "text/html; charset=utf-8", render("add.html", **ctx)


def walkthrough(conn, req, **_):
    default = {"speed": config.DEFAULT_SPEED}
    return _render_add(conn, req, values=default)


def add_submit(conn, req, **_):
    if not req.csrf_ok():
        return _render_add(
            conn, req,
            errors={"form": "Your form session expired. Please try submitting again."},
            values=req.form,
            status=400,
        )

    form = req.form
    values = {
        "url": (form.get("url") or "").strip(),
        "name": (form.get("name") or "").strip(),
        "submitter": (form.get("submitter") or "").strip(),
        "description": (form.get("description") or "").strip(),
        "notes": (form.get("notes") or "").strip(),
        "speed": (form.get("speed") or config.DEFAULT_SPEED).strip().lower(),
    }
    errors: dict[str, str] = {}

    normalized, url_error = _validate_url(values["url"])
    if url_error:
        errors["url"] = url_error
    if values["speed"] not in config.CRAWL_PROFILES:
        values["speed"] = config.DEFAULT_SPEED
    if len(values["name"]) > 120:
        errors["name"] = "Please use a shorter name (120 characters or fewer)."
    if len(values["submitter"]) > 80:
        errors["submitter"] = "Please use a shorter name (80 characters or fewer)."
    if len(values["description"]) > 300:
        errors["description"] = "Please keep the description under 300 characters."
    if len(values["notes"]) > 2000:
        errors["notes"] = "Please keep notes under 2,000 characters."

    if not httrack.available():
        errors["form"] = (
            "The HTTrack website copier is not available on this machine. "
            "Ask an administrator to install it before adding sites."
        )

    active = db.scalar(
        conn,
        "SELECT COUNT(*) FROM mirrors "
        "WHERE status IN ('queued','starting','running','paused')",
    ) or 0
    if active >= config.MAX_QUEUE:
        errors["form"] = "The download queue is full right now. Please try again later."

    duplicate = None
    if normalized and not errors:
        duplicate = _duplicate(conn, normalized, values["url"])
        if duplicate:
            errors["url"] = f"This site is already in the depot as “{duplicate['name']}”."

    if errors:
        return _render_add(
            conn, req, errors=errors, values=values, status=400,
            duplicate=duplicate,
        )

    name = values["name"] or (urlparse(normalized).hostname or "Saved site")
    slug = _slugify(name)
    base = slug
    counter = 2
    while db.one(conn, "SELECT id FROM mirrors WHERE slug=?", (slug,)):
        slug = f"{base}-{counter}"
        counter += 1

    output_dir = str(config.MIRRORS_ROOT / slug)
    cursor = conn.execute(
        "INSERT INTO mirrors(slug, name, url, description, submitter_name, notes, "
        "status, dir_name, output_dir, speed, created_at, updated_at) "
        "VALUES(?, ?, ?, ?, ?, ?, 'queued', ?, ?, ?, datetime('now'), datetime('now'))",
        (
            slug, name, normalized, values["description"], values["submitter"],
            values["notes"], slug, output_dir, values["speed"],
        ),
    )
    conn.commit()
    mirror_id = cursor.lastrowid
    httrack.enqueue(conn, int(mirror_id))
    flash(req, f"Added “{name}”. It is starting now and will appear below.", "ok")
    return redirect("/working")


def _action_redirect(req, message, level="ok", location="/working"):
    flash(req, message, level)
    return redirect(location)


def start_job(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    mirror_id = int(id)
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return _action_redirect(req, "That site was not found.", "error")
    if row["status"] == "paused":
        ok, message = httrack.resume(conn, mirror_id)
    elif row["status"] in ("failed", "cancelled"):
        ok = httrack.retry(conn, mirror_id)
        message = "Queued for another try." if ok else "That site could not be retried."
    elif row["status"] == "queued":
        httrack.ensure_worker()
        ok, message = True, "This site is already waiting in the queue."
    else:
        ok, message = False, "This site is already downloading."
    return _action_redirect(req, message, "ok" if ok else "error")


def pause_job(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    ok, message = httrack.pause(conn, int(id))
    return _action_redirect(req, message, "ok" if ok else "error")


def resume_job(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    ok, message = httrack.resume(conn, int(id))
    return _action_redirect(req, message, "ok" if ok else "error")


def stop_job(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    ok, message = httrack.cancel(conn, int(id))
    return _action_redirect(req, message, "ok" if ok else "error")


def retry_job(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    ok = httrack.retry(conn, int(id))
    return _action_redirect(
        req,
        "Queued for another try." if ok else "This site cannot be retried.",
        "ok" if ok else "error",
    )


def view_log(conn, req, id, **_):
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (int(id),))
    if not row:
        return 404, "text/html; charset=utf-8", "not found"
    lines = httrack.read_log(row).splitlines()[-300:]
    ctx = page_context(conn, req, title="Download log", mirror=dict(row), lines=lines)
    return 200, "text/html; charset=utf-8", render("log.html", **ctx)
