"""Add site walkthrough."""
from __future__ import annotations

import re
from urllib.parse import urlparse

from .. import config, db
from ..services import httrack
from ..web import render
from . import flash, page_context, redirect


def register(add):
    add("GET", re.compile(r"^/add$"), walkthrough)
    add("POST", re.compile(r"^/add$"), add_submit)
    add("POST", re.compile(r"^/start/(?P<id>\d+)$"), start_job)
    add("POST", re.compile(r"^/stop/(?P<id>\d+)$"), stop_job)


def _slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return s or "site"


def walkthrough(conn, req, **_):
    ctx = page_context(conn, req, title="Add a site to mirror")
    return 200, "text/html; charset=utf-8", render("add.html", **ctx)


def add_submit(conn, req, **_):
    if not req.csrf_ok():
        flash(req, "Security check failed. Please try again.", "error")
        return redirect("/add")
    form = req.form
    url = (form.get("url") or "").strip()
    name = (form.get("name") or "").strip()
    submitter = (form.get("submitter") or "").strip()
    notes = (form.get("notes") or "").strip()
    description = (form.get("description") or "").strip()
    speed = (form.get("speed") or "slow").strip().lower()

    if not url:
        flash(req, "Please enter the website address (URL) you want to save.", "error")
        return redirect("/add")
    # basic validation
    if not url.lower().startswith("http://") and not url.lower().startswith("https://"):
        flash(req, "URL must start with http:// or https://. Please add it.", "error")
        return redirect("/add")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        flash(req, "That URL doesn't look right. It should start with http:// or https://", "error")
        return redirect("/add")
    if not name:
        # derive from domain
        name = parsed.netloc

    slug = _slugify(name)
    # ensure unique slug
    base = slug
    i = 2
    while db.one(conn, "SELECT id FROM mirrors WHERE slug=?", (slug,)):
        slug = f"{base}-{i}"
        i += 1

    dir_name = slug
    output_dir = str(config.MIRRORS_ROOT / dir_name)

    conn.execute(
        "INSERT INTO mirrors(slug,name,url,description,submitter_name,notes,status,dir_name,output_dir,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))",
        (slug, name, url, description, submitter, notes, 'queued', dir_name, output_dir),
    )
    conn.commit()
    row = db.one(conn, "SELECT id FROM mirrors WHERE slug=?", (slug,))
    mid = row['id'] if row else None
    flash(req, f"Added '{name}' - starting download now (gentle speed).", "ok")
    if mid:
        try:
            httrack.start_mirror(conn, mid, speed=speed)
        except Exception as e:
            flash(req, f"Could not start automatically: {e}", "error")
    return redirect("/working")


def start_job(conn, req, id, **_):
    if not req.csrf_ok():
        flash(req, "Security check failed.", "error")
        return redirect("/")
    try:
        httrack.start_mirror(conn, int(id))
        flash(req, "Started downloading.", "ok")
    except Exception as e:
        flash(req, f"Could not start: {e}", "error")
    return redirect("/")


def stop_job(conn, req, id, **_):
    if not req.csrf_ok():
        flash(req, "Security check failed.", "error")
        return redirect("/")
    try:
        httrack.stop_mirror(conn, int(id))
        flash(req, "Stopped.", "ok")
    except Exception as e:
        flash(req, f"Could not stop: {e}", "error")
    return redirect("/")
