"""Logs page: list every saved site and show why previous runs failed."""
from __future__ import annotations

import re

from .. import crawl_options, db
from ..web import render
from . import page_context


def register(add):
    add("GET", re.compile(r"^/logs$"), logs_index)


def logs_index(conn, req, **_):
    rows = db.rows(
        conn,
        "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, COALESCE(s.bytes_saved,0) bytes_saved, "
        "COALESCE(s.rate_bps,0) rate_bps "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id "
        "ORDER BY m.updated_at DESC, m.id DESC",
    )
    mirrors = []
    for row in rows:
        item = dict(row)
        item["option_summary"] = crawl_options.summary(item["speed"], item["options_json"])
        mirrors.append(item)

    ctx = page_context(
        conn,
        req,
        title="Logs",
        mirrors=mirrors,
    )
    return 200, "text/html; charset=utf-8", render("logs.html", **ctx)
