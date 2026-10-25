"""Bulk actions for managing multiple mirrors and the queue."""
from __future__ import annotations

import re

from .. import db
from ..services import httrack
from . import add, flash, redirect


def register(add):
    add("POST", re.compile(r"^/bulk/action$"), bulk_action)


def _ids(req):
    return [int(v) for v in req.form.getlist("ids") if v.isdigit()]


def bulk_action(conn, req, **_):
    if not req.csrf_ok():
        return _action_redirect(req, "Security check failed. Please try again.", "error")
    action = (req.form.get("action") or "").strip()
    ids = _ids(req)
    if not ids:
        return _action_redirect(req, "No sites selected.", "error")

    ok_count = 0
    messages = []
    for mirror_id in ids:
        row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
        if not row:
            messages.append(f"#{mirror_id}: not found")
            continue
        try:
            if action == "retry":
                ok = httrack.retry(conn, mirror_id)
                if ok:
                    ok_count += 1
                messages.append(f"{row['name']}: queued" if ok else f"{row['name']}: cannot retry")
            elif action == "pause":
                ok, msg = httrack.pause(conn, mirror_id)
                if ok:
                    ok_count += 1
                messages.append(f"{row['name']}: paused" if ok else f"{row['name']}: {msg}")
            elif action == "resume":
                ok, msg = httrack.resume(conn, mirror_id)
                if ok:
                    ok_count += 1
                messages.append(f"{row['name']}: resumed" if ok else f"{row['name']}: {msg}")
            elif action == "stop":
                ok, msg = httrack.cancel(conn, mirror_id)
                if ok:
                    ok_count += 1
                messages.append(f"{row['name']}: stopped" if ok else f"{row['name']}: {msg}")
            elif action == "remove":
                if row["status"] in add._ACTIVE_STATUSES:
                    messages.append(f"{row['name']}: stop before removing")
                    continue
                ok, msg = add._delete_saved_files(row)
                if not ok:
                    messages.append(f"{row['name']}: {msg}")
                    continue
                conn.execute("DELETE FROM mirrors WHERE id=?", (mirror_id,))
                conn.commit()
                ok_count += 1
                messages.append(f"{row['name']}: removed")
            else:
                messages.append(f"#{mirror_id}: unknown action")
        except Exception as exc:
            messages.append(f"{row['name']}: {exc}")

    flash(req, f"{ok_count} site(s) updated: " + "; ".join(messages[:8]), "ok" if ok_count else "error")
    return redirect("/logs")


def _action_redirect(req, message, level="ok", location="/logs"):
    flash(req, message, level)
    return redirect(location)
