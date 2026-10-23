"""Small JSON endpoints used for live status and logs."""
from __future__ import annotations

import json
import re

from .. import db
from ..services import httrack


def register(add):
    add("GET", re.compile(r"^/api/status$"), status)
    add("GET", re.compile(r"^/api/mirror/(?P<id>\d+)/logs$"), logs)


def _json(payload, status=200):
    return status, "application/json; charset=utf-8", json.dumps(payload)


def status(conn, req, **_):
    running = db.rows(
        conn,
        "SELECT m.id, m.slug, m.name, m.status, m.started_at, "
        "COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, "
        "COALESCE(s.bytes_saved,0) bytes_saved, "
        "COALESCE(s.rate_bps,0) rate_bps "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id "
        "WHERE m.status IN ('starting','running','paused') "
        "ORDER BY m.started_at ASC",
    )
    queued = db.scalar(conn, "SELECT COUNT(*) FROM mirrors WHERE status='queued'") or 0
    completed = db.scalar(conn, "SELECT COUNT(*) FROM mirrors WHERE status='completed'") or 0
    return _json({
        "running": [dict(row) for row in running],
        "queued": queued,
        "completed": completed,
    })


def logs(conn, req, id, **_):
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (int(id),))
    if not row:
        return _json({"error": "not found"}, 404)
    try:
        text = httrack.log_path(row).read_text("utf-8", errors="replace")
    except OSError:
        text = ""
    return _json({"id": row["id"], "name": row["name"], "log": text[-30000:]})
