"""A small HTTP server built on the standard library.

No framework, no dependencies beyond Jinja2. That matters here: the depot has
to boot from a USB stick in a tractor cab with no internet, on a machine
somebody set up five years ago.
"""
from __future__ import annotations

import argparse
import mimetypes
import os
import re
import signal
import socket
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import admin as admin_auth, config, db, views, web

ROUTES: list[tuple[str, re.Pattern[str], object]] = []


def route(pattern: str, method: str = "GET"):
    compiled = re.compile(pattern)

    def decorator(func):
        ROUTES.append((method, compiled, func))
        return func
    return decorator


# Static files live under app/static and are served straight from disk.
STATIC_ROOT = config.STATIC_DIR.resolve()

# Thread local storage for the per thread database connection.
_THREAD_LOCAL = threading.local()


def _local():
    """One database connection per request thread.

    SQLite connections cannot be shared between threads, and the server hands
    every connection to its own thread, so the connection is kept in thread
    local storage and closed with the thread.
    """
    conn = getattr(_THREAD_LOCAL, "conn", None)
    if conn is None:
        conn = db.connect()
        _THREAD_LOCAL.conn = conn
    return conn


class DepotHandler(BaseHTTPRequestHandler):
    server_version = f"RuncheroDepo/{config.SITE_VERSION}"
    protocol_version = "HTTP/1.1"

    # -- plumbing ---------------------------------------------------------
    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write(f"[depo] {self.address_string()} {fmt % args}\n")

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_HEAD(self) -> None:
        self._dispatch("HEAD")

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        if length > config.MAX_FORM_BYTES:
            self.close_connection = True
            self._send(413, "text/plain; charset=utf-8",
                       "That form is too large.\n",
                       extra={"Allow": "GET, HEAD", "Connection": "close"})
            return
        raw = self.rfile.read(length) if length else b""
        content_type = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip()
        if content_type != "application/x-www-form-urlencoded":
            self._send(415, "text/plain; charset=utf-8",
                       "Forms must be application/x-www-form-urlencoded.\n",
                       extra={"Allow": "GET, HEAD"})
            return
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            self._send(400, "text/plain; charset=utf-8", "Bad form encoding.\n")
            return
        parsed_form = parse_qs(text, keep_blank_values=True)
        form = {key: values[-1] if values else ""
                for key, values in parsed_form.items()}
        self._dispatch("POST", form=form)

    # -- routing ----------------------------------------------------------
    def _dispatch(self, method: str, form: dict | None = None) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path) or "/"
        if len(path) > 1 and path.endswith("/"):
            path = path.rstrip("/") or "/"
        query = {k: ",".join(v) for k, v in parse_qs(parsed.query).items()}
        cookies = admin_auth.parse_cookies(self.headers.get("Cookie"))

        if path.startswith("/static/"):
            self._serve_static(path[len("/static/"):])
            return

        try:
            conn = _local()
            for verb, pattern, handler in ROUTES:
                if verb != method and not (verb == "GET" and method == "HEAD"):
                    continue
                match = pattern.match(path)
                if not match:
                    continue
                kwargs = dict(match.groupdict())
                kwargs.update(query)
                kwargs["form"] = form or {}
                kwargs["cookies"] = cookies
                kwargs["client_ip"] = self.client_address[0]
                result = handler(conn, **kwargs)
                self._send_result(result)
                return
            if method == "HEAD":
                self._send(404, "text/plain; charset=utf-8", "")
            else:
                self._send_result(views.not_found(conn))
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            try:
                self._send_result(views.not_found(conn, code=500,
                                                  message="The depot hit a snag."))
            except Exception:
                pass

    # -- responses --------------------------------------------------------
    def _send_result(self, result) -> None:
        if isinstance(result, tuple):
            if len(result) == 3:
                status, headers, body = result
                if isinstance(headers, dict):
                    extra = headers
                    content_type = "text/plain; charset=utf-8"
                else:
                    extra = {}
                    content_type = headers
                self._send(status, content_type, body, extra=extra)
                return
        self._send(200, "text/html; charset=utf-8", result)

    def _send(self, status: int, content_type: str, body, extra=None) -> None:
        if isinstance(body, str):
            payload = body.encode("utf-8")
        elif isinstance(body, (bytes, bytearray)):
            payload = bytes(body)
        else:
            payload = str(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        headers = dict(extra or {})
        if self.path.startswith("/admin"):
            headers.setdefault("Cache-Control", "no-store")
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _serve_static(self, relative: str) -> None:
        target = (STATIC_ROOT / relative).resolve()
        try:
            target.relative_to(STATIC_ROOT)
        except ValueError:
            self._send(403, "text/plain; charset=utf-8", "forbidden")
            return
        if not target.exists() or not target.is_file():
            self._send(404, "text/plain; charset=utf-8", "not found")
            return
        guessed, _ = mimetypes.guess_type(str(target))
        content_type = guessed or "application/octet-stream"
        if content_type.startswith("text/") or content_type in (
                "application/javascript", "application/json",
                "application/manifest+json"):
            content_type += "; charset=utf-8"
        cache = "public, max-age=86400" if target.suffix != ".html" else "no-cache"
        self._send(200, content_type, target.read_bytes(),
                   extra={"Cache-Control": cache})


# --------------------------------------------------------------------------
# route table
# --------------------------------------------------------------------------
def register_routes() -> None:
    ROUTES.clear()
    add = ROUTES.append
    add(("GET", re.compile(r"^/$"), views.home))
    add(("GET", re.compile(r"^/grow$"), views.grow))
    add(("GET", re.compile(r"^/grow/(?P<slug>[a-z0-9-]+)$"),
         lambda conn, slug, **kw: views.collection_page(
             conn, slug, expected_kind="crop", **kw)))
    add(("GET", re.compile(r"^/animals$"), views.animals))
    add(("GET", re.compile(r"^/animals/(?P<slug>[a-z0-9-]+)$"),
         lambda conn, slug, **kw: views.collection_page(
             conn, slug, expected_kind="animal", **kw)))
    add(("GET", re.compile(r"^/kitchen$"), views.kitchen))
    add(("GET", re.compile(r"^/farm$"),
         lambda conn, **kw: views.group_index(conn, "farm", **kw)))
    add(("GET", re.compile(r"^/workshop$"),
         lambda conn, **kw: views.group_index(conn, "workshop", **kw)))
    add(("GET", re.compile(r"^/survival$"),
         lambda conn, **kw: views.group_index(conn, "survival", **kw)))
    add(("GET", re.compile(r"^/home$"),
         lambda conn, **kw: views.group_index(conn, "home", **kw)))
    add(("GET", re.compile(r"^/topic/(?P<slug>[a-z0-9-]+)$"),
         lambda conn, slug, **kw: views.collection_page(
             conn, slug, expected_kind="topic", **kw)))
    add(("GET", re.compile(r"^/(?:collections|topics)$"), views.topics))
    add(("GET", re.compile(r"^/section/(?P<slug>[a-z0-9-]+)$"), views.old_section))
    add(("GET", re.compile(r"^/a/(?P<slug>[a-z0-9-]+)$"), views.old_article))
    add(("GET", re.compile(r"^/(?:vehicles|repair|equipment)$"), views.vehicle_index))
    add(("GET", re.compile(r"^/vehicles/(?P<slug>[a-z0-9-]+)$"), views.vehicle))
    add(("GET", re.compile(r"^/library$"), views.library))
    add(("GET", re.compile(r"^/library/archive$"), views.archive))
    add(("GET", re.compile(r"^/library/archive/(?P<slug>[a-z0-9-]+)$"), views.book))
    add(("GET", re.compile(r"^/library/community$"),
         lambda conn, **kw: views.redirect("/grow")))
    add(("GET", re.compile(r"^/library/community/(?P<slug>[a-z0-9-]+)$"),
         lambda conn, slug, **kw: views.redirect(f"/search?q={slug.replace('-', ' ')}")))
    add(("GET", re.compile(r"^/(?:submit|library/submit)$"), views.submit))
    add(("POST", re.compile(r"^/(?:submit|library/submit)$"), views.submit_post))
    add(("GET", re.compile(r"^/admin/login$"), views.admin_login))
    add(("POST", re.compile(r"^/admin/login$"), views.admin_login_post))
    add(("POST", re.compile(r"^/admin/logout$"), views.admin_logout))
    add(("GET", re.compile(r"^/admin$"), views.admin_dashboard))
    add(("GET", re.compile(r"^/admin/requests/(?P<request_id>[0-9]+)$"),
         views.admin_request))
    add(("POST", re.compile(r"^/admin/requests/(?P<request_id>[0-9]+)$"),
         views.admin_request_post))
    add(("GET", re.compile(r"^/formulas$"), views.formulas))
    add(("GET", re.compile(r"^/conversions$"), views.conversions))
    add(("GET", re.compile(r"^/sources$"), views.sources))
    add(("GET", re.compile(r"^/hub/ford-tractors$"),
         lambda conn, **kw: views.hub(conn, "ford-tractors", **kw)))
    add(("GET", re.compile(r"^/hub/(?P<slug>[a-z0-9-]+)$"), views.old_hub))
    add(("GET", re.compile(r"^/search$"), views.search))
    add(("GET", re.compile(r"^/read/(?P<slug>[a-z0-9-]+)$"), views.reader))
    add(("GET", re.compile(r"^/download/(?P<slug>[a-z0-9-]+)$"), views.download))
    add(("GET", re.compile(r"^/api/search$"), views.api_search))
    add(("GET", re.compile(r"^/api/stats$"), views.api_stats))
    add(("GET", re.compile(r"^/robots\.txt$"), views.robots))
    add(("GET", re.compile(r"^/manifest\.webmanifest$"), _manifest))
    add(("GET", re.compile(r"^/sw\.js$"), _service_worker))


def _manifest(conn, **_) -> tuple[int, str, str]:
    import json
    payload = {
        "name": config.SITE_NAME,
        "short_name": config.SITE_SHORT,
        "description": config.SITE_TAGLINE,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1b1b23",
        "theme_color": "#6cc24a",
        "icons": [
            {"src": "/static/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/static/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    return 200, "application/manifest+json", json.dumps(payload)


def _service_worker(conn, **_) -> tuple[int, str, str]:
    path = config.STATIC_DIR / "sw.js"
    if not path.exists():
        return 200, "application/javascript", "// no service worker"
    return 200, "application/javascript", path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------
class DepotServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def server_bind(self) -> None:
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()


def build(host: str, port: int) -> DepotServer:
    config.ensure_dirs()
    conn = db.connect()
    db.init_db(conn)
    conn.close()
    register_routes()
    return DepotServer((host, port), DepotHandler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runchero Information Depo")
    parser.add_argument("--host", default=config.DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=config.DEFAULT_PORT)
    parser.add_argument("--seed", action="store_true",
                        help="populate the database before serving")
    args = parser.parse_args(argv)

    if args.seed:
        from .seed import run as seed_run
        seed_run.main([])

    server = build(args.host, args.port)
    shown = "localhost" if args.host in ("0.0.0.0", "") else args.host
    print(f"{config.SITE_NAME} running on http://{shown}:{args.port}")
    print("  press Ctrl+C to stop")

    def shutdown(*_):
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGINT, shutdown)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
