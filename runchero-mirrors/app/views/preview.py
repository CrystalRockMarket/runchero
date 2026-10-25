"""Preview saved mirror files inside the depot."""
from __future__ import annotations

import mimetypes
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

from .. import db
from ..services import httrack
from ..web import render
from . import page_context


def register(add):
    add("GET", re.compile(r"^/preview/(?P<slug>[^/]+)(?:/(?P<path>.*))?$"), preview_file)


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


def _resolve_target(row, rel: str):
    base = Path(row["output_dir"]).resolve()
    entry_path = row["entry_path"] or ""
    serve_root = row["serve_root"] or ""
    if not entry_path:
        entry_path, serve_root = httrack.find_entry(base, row["url"])
        if entry_path:
            conn.execute(
                "UPDATE mirrors SET entry_path=?, serve_root=? WHERE id=?",
                (entry_path, serve_root, row["id"]),
            )
            conn.commit()

    if any(part.startswith(".") for part in rel.split("/") if part) or rel.split("/", 1)[0] == "hts-cache":
        return None, None, None, "That file was not found."

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
    # The user path may still carry the host folder; strip it so we don't
    # double the host directory when resolving the file.
    host_prefix = host_dir + "/"
    if rel.startswith(host_prefix):
        rel = rel[len(host_prefix):]
    site_root = (base / host_dir).resolve()
    try:
        site_root.relative_to(base)
    except ValueError:
        return None, None, None, "Forbidden."

    target = (site_root / rel).resolve()
    if not target.exists():
        fallback = (base / rel).resolve()
        try:
            fallback.relative_to(base)
            target = fallback
        except ValueError:
            pass
    try:
        target.relative_to(base)
    except ValueError:
        return None, None, None, "Forbidden."

    if not target.exists() or not target.is_file():
        return None, None, None, "That saved file was not found."

    return target, entry_rel, site_root, None


def preview_file(conn, req, slug, path=None, **_):
    row = db.one(
        conn,
        "SELECT * FROM mirrors WHERE slug=?",
        (slug,),
    )
    if not row:
        return 404, "text/html; charset=utf-8", "This saved site is not ready yet."

    base = Path(row["output_dir"]).resolve()
    if not base.exists():
        return 404, "text/html; charset=utf-8", "The saved files for this site are missing."

    entry_path = row["entry_path"] or ""
    serve_root = row["serve_root"] or ""
    if not entry_path:
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
        return 400, "text/plain; charset=utf-8", "Bad request."

    # Derive the host-relative entry path for the root redirect.
    entry_rel = entry_path
    serve_root_local = row["serve_root"] or ""
    if serve_root_local and serve_root_local not in ("", "."):
        first = serve_root_local.split("/", 1)[0]
        prefix = first + "/"
        if entry_path.startswith(prefix):
            entry_rel = entry_path[len(prefix):]
        elif entry_path != first:
            entry_rel = entry_path

    if not rel:
        # Start at the entry page so the first preview is useful.
        location = entry_rel
        if location.lower().endswith(tuple("." + n for n in httrack.INDEX_NAMES)):
            location = location.rsplit("/", 1)[0] + "/"
        return 302, {"Location": f"/preview/{slug}/" + quote(location, safe="/")}, ""

    target, entry_rel, site_root, error = _resolve_target(row, rel)
    if error:
        return 404, "text/html; charset=utf-8", error

    ctype, _encoding = mimetypes.guess_type(str(target))
    is_image = bool(ctype and ctype.startswith("image/"))
    is_html = ctype == "text/html" or httrack.looks_like_html(target)
    is_text = bool(
        ctype
        and (
            ctype.startswith("text/")
            or ctype in ("application/javascript", "application/json", "application/xml", "image/svg+xml")
        )
    )
    is_pdf = ctype == "application/pdf"

    mirror_url = f"/mirror/{slug}/" + quote(rel, safe="/")
    parent = str(Path(rel).parent)
    parent_url = f"/preview/{slug}/" + quote(parent + "/", safe="/") if parent else f"/preview/{slug}/"

    try:
        text = target.read_text("utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        text = None

    ctx = page_context(
        conn,
        req,
        title=f"Preview · {row['name']}",
        mirror=dict(row),
        file_name=target.name,
        rel=rel,
        mirror_url=mirror_url,
        parent_url=parent_url,
        is_image=is_image,
        is_html=is_html,
        is_text=is_text,
        is_pdf=is_pdf,
        ctype=ctype or "application/octet-stream",
        text=escape(text or "") if text is not None else None,
        size=target.stat().st_size,
    )
    return 200, "text/html; charset=utf-8", render("preview.html", **ctx)
