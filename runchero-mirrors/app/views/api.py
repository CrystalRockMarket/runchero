"""API for status."""
from __future__ import annotations

import json
import re

from .. import db


def register(add):
    add("GET", re.compile(r"^/api/status$"), status)
    add("GET", re.compile(r"^/api/mirror/(?P<id>\d+)/logs$"), logs)


def status(conn, req, **_):
    running = db.rows(conn, "SELECT m.id,m.slug,m.name,m.status,m.started_at,COALESCE(s.pages_saved,0) pages_saved,COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status='running' ORDER BY m.started_at ASC")
    queued = db.rows(conn, "SELECT count(*) c FROM mirrors WHERE status='queued'")
    completed = db.rows(conn, "SELECT count(*) c FROM mirrors WHERE status='completed'")
    return 200, "application/json; charset=utf-8", json.dumps({
        "running": [dict(r) for r in running],
        "queued": queued[0]['c'] if queued else 0,
        "completed": completed[0]['c'] if completed else 0,
    })


def logs(conn, req, id, **_):
    rows = db.rows(conn, "SELECT line,created_at FROM mirror_logs WHERE mirror_id=? ORDER BY id DESC LIMIT 100", (id,))
    return 200, "application/json; charset=utf-8", json.dumps([dict(r) for r in reversed(rows)])
