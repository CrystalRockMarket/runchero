"""Browse completed mirrors."""
from __future__ import annotations

import os
import re
from pathlib import Path

from .. import config, db
from ..web import render
from . import page_context, redirect


def register(add):
    add("GET", re.compile(r"^/browse$"), list_mirrors)
    add("GET", re.compile(r"^/view/(?P<slug>[^/]+)(?P<sub>.*)$"), view_mirror)
    add("GET", re.compile(r"^/mirror/(?P<slug>[^/]+)(?P<path>.*)$"), serve_mirror_file)


def list_mirrors(conn, req, **_):
    completed = db.rows(conn, "SELECT m.*, COALESCE(s.pages_saved,0) pages_saved, COALESCE(s.files_saved,0) files_saved FROM mirrors m LEFT JOIN mirror_stats s ON s.mirror_id=m.id WHERE m.status='completed' ORDER BY m.finished_at DESC")
    ctx = page_context(conn, req, completed=[dict(x) for x in completed], title="Browse saved sites")
    return 200, "text/html; charset=utf-8", render("browse.html", **ctx)


def view_mirror(conn, req, slug, sub="", **_):
    row = db.one(conn, "SELECT * FROM mirrors WHERE slug=? AND status='completed'", (slug,))
    if not row:
        return redirect("/browse")
    base = Path(row['output_dir']).resolve()
    if not base.exists():
        return redirect("/browse")
    # determine file to serve
    if not sub or sub == "/":
        # try common index files
        for cand in ["index.html", "index.htm", "home.html"]:
            p = base / cand
            if p.exists():
                subpath = cand
                break
        else:
            # look for first html
            found = None
            for root, dirs, files in os.walk(base):
                for f in files:
                    if f.endswith(('.html', '.htm')):
                        found = os.path.relpath(os.path.join(root, f), base)
                        break
                if found:
                    break
            subpath = found or "index.html"
    else:
        subpath = sub.lstrip("/")
    target = (base / subpath).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        return redirect("/browse")
    if not target.exists() or not target.is_file():
        # try index in dir
        if target.is_dir():
            for cand in ["index.html", "index.htm"]:
                p2 = target / cand
                if p2.exists():
                    target = p2.resolve()
                    break
        if not target.exists():
            return redirect(f"/view/{slug}")
    # read and serve as html with base path adjusted? keep simple - serve file
    try:
        data = target.read_bytes()
    except Exception:
        return redirect("/browse")
    # determine content type
    import mimetypes
    ctype, _ = mimetypes.guess_type(str(target))
    if not ctype:
        ctype = "text/html" if target.suffix in ('.html', '.htm') else "application/octet-stream"
    if ctype.startswith('text/') or ctype in ('application/javascript', 'application/json'):
        ctype += "; charset=utf-8"
    # for local browsing, we need to make links work relative - but easier to serve from /mirror-files/; simpler approach: iframe or serve files under /mirror-static/
    # implement simple file server under /files/<slug>/
    # but we registered pattern with sub; better to redirect to a file serving route
    # quick fix: serve directly
    headers = {"Content-Type": ctype}
    return 200, headers, data


# Add file serving route
from ..httpd import route


def register_files(add):
    add("GET", re.compile(r"^/mirror/(?P<slug>[^/]+)(?P<path>.*)$"), serve_mirror_file)


def serve_mirror_file(conn, req, slug, path="", **_):
    row = db.one(conn, "SELECT * FROM mirrors WHERE slug=? AND status='completed'", (slug,))
    if not row:
        return 404, "text/plain; charset=utf-8", "not found"
    base = Path(row['output_dir']).resolve()
    if not base.exists():
        return 404, "text/plain; charset=utf-8", "not found"
    rel = path.lstrip("/") or "index.html"
    target = (base / rel).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        return 403, "text/plain; charset=utf-8", "forbidden"
    if target.is_dir():
        for cand in ["index.html", "index.htm", "index.php"]:
            p2 = target / cand
            if p2.exists():
                target = p2
                break
    if not target.exists() or not target.is_file():
        return 404, "text/plain; charset=utf-8", "not found"
    import mimetypes
    ctype, _ = mimetypes.guess_type(str(target))
    if not ctype:
        ctype = "application/octet-stream"
    if ctype.startswith('text/') or ctype in ('application/javascript', 'application/json', 'application/xml'):
        ctype += "; charset=utf-8"
    try:
        data = target.read_bytes()
    except Exception:
        return 404, "text/plain; charset=utf-8", "not found"
    return 200, {"Content-Type": ctype, "Cache-Control": "public, max-age=3600"}, data
