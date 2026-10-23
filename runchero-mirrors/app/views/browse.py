"""Browse finished mirrors and serve their files."""
from __future__ import annotations

import mimetypes
import re
from pathlib import Path
from urllib.parse import quote

from .. import db
from ..services import httrack
from ..web import FilePayload, render
from . import page_context


def register(add):
    add("GET", re.compile(r"^/browse$"), list_mirrors)
    add("GET", re.compile(r"^/mirror/(?P<slug>[^/]+)(?:/(?P<path>.*))?$"), serve_mirror)


def list_mirrors(conn, req, **_):
    completed = []
    for row in db.rows(
        conn,
        "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, "
        "COALESCE(s.files_saved,0) files_saved, COALESCE(s.bytes_saved,0) bytes_saved "
        "FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id "
        "WHERE m.status='completed' ORDER BY m.finished_at DESC, m.id DESC",
    ):
        completed.append(dict(row))
    ctx = page_context(conn, req, title="Browse saved sites", completed=completed)
    return 200, "text/html; charset=utf-8", render("browse.html", **ctx)


def _safe_relative(value: str | None) -> str:
    value = (value or "").replace("\\", "/").lstrip("/")
    parts = []
    for part in value.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            return ""
        parts.append(part)
    return "/".join(parts)


def _looks_like_dir(path: Path) -> bool:
    return path.exists() and path.is_dir()


def serve_mirror(conn, req, slug, path=None, **_):
    row = db.one(
        conn,
        "SELECT * FROM mirrors WHERE slug=? AND status='completed'",
        (slug,),
    )
    if not row:
        return 404, "text/html; charset=utf-8", "This saved site is not ready yet."
    base = Path(row["output_dir"]).resolve()
    if not base.exists():
        return 404, "text/html; charset=utf-8", "The saved files for this site are missing."

    serve_root = row["serve_root"] or ""
    entry_path = row["entry_path"] or ""
    if not entry_path:
        # Older rows and hand-copied mirrors: discover the front page now.
        entry_path, serve_root = httrack.find_entry(base, row["url"])
        if entry_path:
            conn.execute(
                "UPDATE mirrors SET entry_path=?, serve_root=? WHERE id=?",
                (entry_path, serve_root, row["id"]),
            )
            conn.commit()
    if not entry_path:
        return 404, "text/html; charset=utf-8", "This saved site has no readable front page."

    rel = _safe_relative(path)
    if "\x00" in rel:
        return 400, "text/html; charset=utf-8", "Bad request."
    if not serve_root:
        serve_root = "."
    root_path = (base / serve_root).resolve()
    try:
        root_path.relative_to(base)
    except ValueError:
        return 403, "text/html; charset=utf-8", "Forbidden."

    if not rel:
        target = (base / entry_path).resolve()
    else:
        target = (root_path / rel).resolve()
        if not target.exists():
            # Absolute links from a site saved under a subfolder should point at
            # the site root, not the start folder. Also accept a mirror-root
            # fallback for sites that were saved with a different layout.
            fallbacks = []
            host_dir = serve_root.split("/", 1)[0]
            if host_dir and host_dir != ".":
                fallbacks.append(base / host_dir / rel)
            fallbacks.append(base / rel)
            for fallback in fallbacks:
                fallback = fallback.resolve()
                try:
                    fallback.relative_to(base)
                except ValueError:
                    continue
                if fallback.exists():
                    target = fallback
                    break

    try:
        target.relative_to(base)
    except ValueError:
        return 403, "text/html; charset=utf-8", "Forbidden."

    if _looks_like_dir(target):
        if rel and not rel.endswith("/") and not req.path.endswith("/"):
            return 301, {"Location": quote(req.path + "/", safe="/%")}, ""
        for candidate in ("index.html", "index.htm", "index.xhtml"):
            index = (target / candidate).resolve()
            if index.is_file():
                target = index
                break
        else:
            return 404, "text/html; charset=utf-8", "No index page in this folder."

    if not target.exists() or not target.is_file():
        return 404, "text/html; charset=utf-8", "That saved page or file was not found."

    ctype, _encoding = mimetypes.guess_type(str(target))
    if not ctype:
        ctype = "text/html" if target.suffix.lower() in (".html", ".htm") else "application/octet-stream"
    if ctype.startswith("text/") or ctype in (
        "application/javascript", "application/json", "application/xml",
        "image/svg+xml",
    ):
        ctype += "; charset=utf-8"
    return 200, "text/html; charset=utf-8", FilePayload(
        path=target,
        content_type=ctype,
        extra={"Cache-Control": "public, max-age=300"},
    )
