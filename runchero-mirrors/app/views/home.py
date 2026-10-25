"""Dashboard and the Currently working page."""
from __future__ import annotations

import datetime as dt
import re

from .. import db
from ..web import render
from . import page_context

_ACTIVE_STATUSES = ("queued", "starting", "running", "paused")


def register(add):
    add("GET", re.compile(r"^/$"), index)
    add("GET", re.compile(r"^/dashboard$"), index)
    add("GET", re.compile(r"^/working$"), working)


def _seconds(started_at: str | None, finished_at: str | None = None) -> int:
    if not started_at:
        return 0
    try:
        start = dt.datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S")
        end = (
            dt.datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S")
            if finished_at else dt.datetime.utcnow()
        )
        return max(0, int((end - start).total_seconds()))
    except (TypeError, ValueError):
        return 0


def _decorate(rows) -> list[dict]:
    out = []
    for row in rows:
        item = dict(row)
        seconds = _seconds(item.get("started_at"), item.get("finished_at"))
        pages = int(item.get("pages_saved") or 0)
        total_bytes = int(item.get("bytes_saved") or 0)
        item["elapsed_seconds"] = seconds
        item["pages_per_minute"] = (
            round(pages / (seconds / 60), 1) if seconds >= 20 and pages else 0
        )
        item["average_rate"] = int(total_bytes / seconds) if seconds else 0
        out.append(item)
    return out


def _active(conn):
    return _decorate(db.rows(
        conn,
        "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, COALESCE(s.bytes_saved,0) bytes_saved, "
        "COALESCE(s.rate_bps,0) rate_bps "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id "
        "WHERE m.status IN ('starting','running','paused','queued') "
        "ORDER BY CASE m.status WHEN 'running' THEN 0 WHEN 'paused' THEN 1 "
        "WHEN 'starting' THEN 2 ELSE 3 END, m.created_at ASC",
    ))


def _completed(conn, limit=24):
    return _decorate(db.rows(
        conn,
        "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, COALESCE(s.bytes_saved,0) bytes_saved, "
        "COALESCE(s.rate_bps,0) rate_bps "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id "
        "WHERE m.status='completed' ORDER BY m.finished_at DESC, m.id DESC LIMIT ?",
        (limit,),
    ))


def _failed(conn):
    return _decorate(db.rows(
        conn,
        "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, COALESCE(s.bytes_saved,0) bytes_saved, "
        "COALESCE(s.rate_bps,0) rate_bps "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id "
        "    WHERE m.status IN ('failed','cancelled','crashed') "
        "ORDER BY m.updated_at DESC, m.id DESC LIMIT 12",
    ))


def _counts(conn) -> dict[str, int]:
    counts = {status: 0 for status in _ACTIVE_STATUSES + ("completed", "failed", "cancelled")}
    for row in db.rows(conn, "SELECT status, COUNT(*) n FROM mirrors GROUP BY status"):
        counts[row["status"]] = row["n"]
    counts["active"] = sum(counts[s] for s in _ACTIVE_STATUSES)
    totals = db.one(
        conn,
        "SELECT COALESCE(SUM(s.pages_saved),0) pages, "
        "COALESCE(SUM(s.files_saved),0) files, "
        "COALESCE(SUM(s.bytes_saved),0) bytes "
        "FROM mirror_stats s JOIN mirrors m ON m.id=s.mirror_id "
        "WHERE m.status='completed' OR (m.status='crashed' AND m.entry_path <> '')",
    )
    counts["total_pages"] = int(totals["pages"] if totals else 0)
    counts["total_files"] = int(totals["files"] if totals else 0)
    counts["total_bytes"] = int(totals["bytes"] if totals else 0)
    return counts


def index(conn, req, **_):
    ctx = page_context(
        conn, req,
        title="Dashboard",
        active=_active(conn),
        completed=_completed(conn, limit=8),
        failed=_failed(conn),
        counts=_counts(conn),
    )
    return 200, "text/html; charset=utf-8", render("home.html", **ctx)


def working(conn, req, **_):
    ctx = page_context(
        conn, req,
        title="Currently working",
        active=_active(conn),
        counts=_counts(conn),
    )
    return 200, "text/html; charset=utf-8", render("working.html", **ctx)
