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
        "WHERE m.status='completed' OR (m.status='crashed' AND m.entry_path <> '') "
        "ORDER BY m.finished_at DESC, m.id DESC",
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
        "SELECT * FROM mirrors WHERE slug=? AND status IN ('completed', 'crashed')",
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
    if any(part.startswith(".") for part in rel.split("/") if part) or rel.split("/", 1)[0] == "hts-cache":
        return 404, "text/html; charset=utf-8", "That saved page or file was not found."

    # HTTrack saves a site as <mirror>/<host>/<original path>. Serve the host
    # folder as the site root so root-relative links and relative links with
    # "../" keep the same shape they had on the original site.
    host_dir = "."
    entry_rel = entry_path
    if serve_root and serve_root not in ("", "."):
        first = serve_root.split("/", 1)[0]
        prefix = first + "/"
        if entry_path.startswith(prefix):
            host_dir = first
            entry_rel = entry_path[len(prefix):]
        elif entry_path != first:
            host_dir = first
            entry_rel = entry_path
    site_root = (base / host_dir).resolve()
    try:
        site_root.relative_to(base)
    except ValueError:
        return 403, "text/html; charset=utf-8", "Forbidden."

    if not rel:
        if not req.path.endswith("/"):
            return 301, {"Location": quote(req.path + "/", safe="/")}, ""
        if entry_rel in httrack.INDEX_NAMES:
            target = (site_root / entry_rel).resolve()
        else:
            # Start the browser at the original page path, not the mirror root,
            # so links such as "../" resolve inside the saved copy correctly.
            if any(entry_rel.lower().endswith("/" + name) for name in httrack.INDEX_NAMES):
                location = entry_rel.rsplit("/", 1)[0] + "/"
            else:
                location = entry_rel
            return 302, {"Location": f"/mirror/{slug}/" + quote(location, safe="/")}, ""
    else:
        target = (site_root / rel).resolve()
        if not target.exists():
            # Unexpected layouts (or an entry at the mirror root) can still be
            # served from the mirror root as a safe fallback.
            fallback = (base / rel).resolve()
            try:
                fallback.relative_to(base)
                target = fallback
            except ValueError:
                pass

    try:
        target.relative_to(base)
    except ValueError:
        return 403, "text/html; charset=utf-8", "Forbidden."

    if _looks_like_dir(target):
        if rel and not req.path.endswith("/"):
            return 301, {"Location": quote(req.path + "/", safe="/")}, ""
        for candidate in httrack.INDEX_NAMES:
            index = (target / candidate).resolve()
            if index.is_file():
                target = index
                break
        else:
            return 404, "text/html; charset=utf-8", "No index page in this folder."

    try:
        target.relative_to(base)
    except ValueError:
        return 403, "text/html; charset=utf-8", "Forbidden."

    if not target.exists() or not target.is_file():
        return 404, "text/html; charset=utf-8", "That saved page or file was not found."

    ctype, _encoding = mimetypes.guess_type(str(target))
    entry_file = (base / entry_path).resolve()
    is_page = (
        target == entry_file
        or target.suffix.lower() in httrack.PAGE_SUFFIXES
        or (ctype in (None, "application/octet-stream") and httrack.looks_like_html(target))
    )
    if is_page:
        ctype = "text/html"
    elif not ctype:
        ctype = "application/octet-stream"
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
