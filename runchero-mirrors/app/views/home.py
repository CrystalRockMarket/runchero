"""Home/Dashboard overview."""
from __future__ import annotations

import re
from datetime import datetime

from .. import db
from ..web import render
from . import page_context


def register(add):
    add("GET", re.compile(r"^/$"), index)
    add("GET", re.compile(r"^/dashboard$"), dashboard)
    add("GET", re.compile(r"^/working$"), working)


def _fmt_duration(started_at, finished_at=None):
    try:
        if not started_at:
            return "—"
        start = datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S") if finished_at else datetime.utcnow()
        delta = int((end - start).total_seconds())
        if delta < 0:
            delta = 0
        h = delta // 3600
        m = (delta % 3600) // 60
        s = delta % 60
        if h > 0:
            return f"{h}h {m}m {s}s"
        if m > 0:
            return f"{m}m {s}s"
        return f"{s}s"
    except Exception:
        return "—"


def index(conn, req, **_):
    queued = db.rows(conn, "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status='queued' ORDER BY m.created_at ASC")
    running = db.rows(conn, "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status='running' ORDER BY m.started_at ASC")
    completed = db.rows(conn, "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status='completed' ORDER BY m.finished_at DESC LIMIT 50")
    failed = db.rows(conn, "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status IN ('failed','cancelled') ORDER BY m.updated_at DESC LIMIT 20")

    for r in running:
        r = dict(r)
    # attach durations
    run_list = []
    for r in running:
        d = dict(r)
        d['duration'] = _fmt_duration(d['started_at'])
        run_list.append(d)
    comp_list = []
    for r in completed:
        d = dict(r)
        d['duration'] = _fmt_duration(d['started_at'], d['finished_at'])
        comp_list.append(d)
    fail_list = []
    for r in failed:
        d = dict(r)
        d['duration'] = _fmt_duration(d['started_at'], d['finished_at'])
        fail_list.append(d)

    ctx = page_context(conn, req,
                       queued=[dict(x) for x in queued],
                       running=run_list,
                       completed=comp_list,
                       failed=fail_list,
                       title="Dashboard")
    return 200, "text/html; charset=utf-8", render("home.html", **ctx)


dashboard = index


def working(conn, req, **_):
    running = db.rows(conn, "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status IN ('running','queued') ORDER BY CASE WHEN m.status='running' THEN 0 ELSE 1 END, m.started_at ASC, m.created_at ASC")
    run_list = []
    for r in running:
        d = dict(r)
        d['duration'] = _fmt_duration(d['started_at']) if d['started_at'] else 'starting...'
        run_list.append(d)
    ctx = page_context(conn, req, running=run_list, title="Currently working")
    return 200, "text/html; charset=utf-8", render("working.html", **ctx)
