"""Guided add-site walkthrough and mirror controls."""
from __future__ import annotations

import ipaddress
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from .. import config, crawl_options, db
from ..services import httrack
from ..web import render
from . import flash, page_context, redirect

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_ACTIVE_STATUSES = ("queued", "starting", "running", "paused")
_ADVANCED_ERRORS = {
    "depth", "rate_kbps", "max_size_mb", "max_hours", "sockets",
    "timeout", "retries", "robots", "scope",
}


def register(add):
    add("GET", re.compile(r"^/add$"), walkthrough)
    add("POST", re.compile(r"^/add$"), add_submit)
    add("GET", re.compile(r"^/rerun/(?P<id>\d+)$"), rerun_form)
    add("POST", re.compile(r"^/rerun/(?P<id>\d+)$"), rerun_submit)
    add("POST", re.compile(r"^/remove/(?P<id>\d+)$"), remove_mirror)
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


def _url_key(value: str):
    try:
        parsed = urlparse(value)
        port = parsed.port
    except ValueError:
        return value.lower()
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        host = f"{host}:{port}"
    return (scheme, host, parsed.path or "/", parsed.query)


def _duplicate(conn, normalized: str):
    wanted = _url_key(normalized)
    rows = db.rows(
        conn,
        "SELECT id, name, slug, url, status FROM mirrors "
        "ORDER BY CASE status "
        "WHEN 'running' THEN 0 WHEN 'paused' THEN 1 WHEN 'starting' THEN 2 "
        "WHEN 'queued' THEN 3 WHEN 'completed' THEN 4 ELSE 5 END, id DESC",
    )
    for row in rows:
        if _url_key(row["url"]) == wanted:
            return row
    return None


def _active_tab(errors) -> str:
    return "advanced" if any(key in errors for key in _ADVANCED_ERRORS) else "basic"


def _render_add(
    conn, req, *, errors=None, values=None, status=200, duplicate=None,
    mode="add", mirror=None,
):
    errors = errors or {}
    values = values or crawl_options.form_values(config.DEFAULT_SPEED)
    speed = values.get("speed") or config.DEFAULT_SPEED
    raw_options = mirror["options_json"] if mirror else None
    action = f"/rerun/{mirror['id']}" if mirror else "/add"
    ctx = page_context(
        conn,
        req,
        title="Rerun a site" if mirror else "Add a site",
        errors=errors,
        values=values,
        duplicate=duplicate,
        mode=mode,
        mirror=mirror,
        action=action,
        active_tab=_active_tab(errors),
        advanced_defaults=crawl_options.summary(speed, raw_options),
    )
    return status, "text/html; charset=utf-8", render("add.html", **ctx)


def walkthrough(conn, req, **_):
    return _render_add(conn, req, values={"speed": config.DEFAULT_SPEED})


def add_submit(conn, req, **_):
    form = req.form
    if not req.csrf_ok():
        return _render_add(
            conn, req,
            errors={"form": "Your form session expired. Please try submitting again."},
            values=form,
            status=400,
        )

    options, option_values, option_errors = crawl_options.parse_form(form)
    values = {
        "url": (form.get("url") or "").strip(),
        "name": (form.get("name") or "").strip(),
        "submitter": (form.get("submitter") or "").strip(),
        "description": (form.get("description") or "").strip(),
        "notes": (form.get("notes") or "").strip(),
        **option_values,
    }
    errors: dict[str, str] = dict(option_errors)

    normalized, url_error = _validate_url(values["url"])
    if url_error:
        errors["url"] = url_error
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
    save_anyway = form.get("confirm_duplicate") == "1"
    if normalized and not errors:
        duplicate = _duplicate(conn, normalized)
        if duplicate and not save_anyway:
            return _render_add(
                conn, req, values=values, duplicate=duplicate, status=200,
            )

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
        "status, dir_name, output_dir, speed, options_json, created_at, updated_at) "
        "VALUES(?, ?, ?, ?, ?, ?, 'queued', ?, ?, ?, ?, datetime('now'), datetime('now'))",
        (
            slug, name, normalized, values["description"], values["submitter"],
            values["notes"], slug, output_dir, values["speed"],
            crawl_options.dump(options),
        ),
    )
    conn.commit()
    mirror_id = cursor.lastrowid
    httrack.enqueue(conn, int(mirror_id))
    message = f"Added “{name}”. It is starting now and will appear below."
    if duplicate and save_anyway:
        message = f"Added another copy of “{name}”."
    flash(req, message, "ok")
    return redirect("/working")


def _rerunnable(row) -> bool:
    return row is not None and row["status"] in ("completed", "failed", "cancelled", "crashed")


def rerun_form(conn, req, id, **_):
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (int(id),))
    if not row:
        return _action_redirect(req, "That site was not found.", "error")
    if not _rerunnable(row):
        return _action_redirect(
            req, "That site is still working. Pause or stop it before rerunning.",
            "error",
        )
    values = crawl_options.form_values(row["speed"], row["options_json"], rerun=True)
    return _render_add(
        conn, req, values=values, mode="rerun", mirror=dict(row),
    )


def rerun_submit(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    mirror_id = int(id)
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return _action_redirect(req, "That site was not found.", "error")
    if not _rerunnable(row):
        return _action_redirect(
            req, "That site is still working. Pause or stop it before rerunning.",
            "error",
        )

    options, values, errors = crawl_options.parse_form(req.form, rerun=True)
    if errors:
        return _render_add(
            conn, req, errors=errors, values=values, status=400,
            mode="rerun", mirror=dict(row),
        )

    ok, message = httrack.rerun(
        conn, mirror_id, values["speed"], crawl_options.dump(options),
    )
    if ok:
        message = f"Queued “{row['name']}” again with the new settings."
    return _action_redirect(req, message, "ok" if ok else "error")


def _delete_saved_files(row) -> tuple[bool, str]:
    root = config.MIRRORS_ROOT.resolve()
    outdir = Path(row["output_dir"])
    folders = [
        outdir,
        config.MIRRORS_ROOT / ".cache" / row["slug"],
    ]
    files = [config.MIRRORS_ROOT / ".cache" / f"{row['slug']}.log"]

    targets: list[Path] = []
    for target in folders + files:
        try:
            resolved = target.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            return False, "The saved files are outside the depot folder. Nothing was deleted."
        if resolved == root:
            return False, "The saved folder is not safe to delete. Nothing was deleted."
        targets.append(target)

    try:
        for target in targets:
            if target.is_symlink():
                target.unlink()
            elif target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
    except OSError as exc:
        return False, f"Could not delete every saved file: {exc}"
    return True, ""


def remove_mirror(conn, req, id, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    mirror_id = int(id)
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return _action_redirect(req, "That site was not found.", "error")
    if row["status"] in _ACTIVE_STATUSES:
        return _action_redirect(
            req, "Stop that download before removing it.", "error",
        )

    ok, message = _delete_saved_files(row)
    if not ok:
        return _action_redirect(req, message, "error")
    conn.execute("DELETE FROM mirrors WHERE id=?", (mirror_id,))
    conn.commit()
    flash(req, f"Removed “{row['name']}” and its saved files.", "ok")
    return redirect("/browse" if row["status"] == "completed" else "/")


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
    elif row["status"] in ("failed", "cancelled", "crashed"):
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
    row = db.one(
        conn,
        "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, COALESCE(s.bytes_saved,0) bytes_saved "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.id=?",
        (int(id),),
    )
    if not row:
        return 404, "text/html; charset=utf-8", "not found"
    lines = httrack.read_log(row).splitlines()[-300:]
    ctx = page_context(
        conn, req,
        title="Download log",
        mirror=dict(row),
        lines=lines,
        option_summary=crawl_options.summary(row["speed"], row["options_json"]),
    )
    return 200, "text/html; charset=utf-8", render("log.html", **ctx)
