"""A small HTTP server built on the standard library.

No framework, no dependencies beyond Jinja2. The shop has to boot on the same
kind of box the depot boots on, with no internet and no package installs.

This is the depot's server with writes allowed: forms POST, sessions are
signed cookies, and static files are still served straight from disk.
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

from . import config, db, views
from .web import Request

ROUTES: list[tuple[str, re.Pattern[str], object]] = []

#: Static files live under app/static and are served straight from disk.
STATIC_ROOT = config.STATIC_DIR.resolve()

#: Thread local storage for the per thread database connection.
_THREAD_LOCAL = threading.local()


def route(pattern: str, method: str = "GET"):
    compiled = re.compile(pattern)

    def decorator(func):
        ROUTES.append((method, compiled, func))
        return func
    return decorator


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


class ShopHandler(BaseHTTPRequestHandler):
    server_version = f"RuncheroShop/{config.SITE_VERSION}"
    protocol_version = "HTTP/1.1"

    # -- plumbing ---------------------------------------------------------
    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write(f"[shop] {self.address_string()} {fmt % args}\n")

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_HEAD(self) -> None:
        self._dispatch("HEAD")

    def do_POST(self) -> None:
        self._dispatch("POST")

    def do_PUT(self) -> None:
        self._dispatch("PUT")

    def do_DELETE(self) -> None:
        self._dispatch("DELETE")

    # -- routing ----------------------------------------------------------
    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path) or "/"
        if len(path) > 1 and path.endswith("/"):
            path = path.rstrip("/") or "/"
        query = {k: ",".join(v) for k, v in parse_qs(parsed.query).items()}

        if path.startswith("/static/"):
            self._serve_static(path[len("/static/"):])
            return

        body = b""
        if method in ("POST", "PUT", "DELETE"):
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                length = 0
            length = max(0, min(length, config.MAX_REQUEST_BYTES))
            if length:
                body = self.rfile.read(length)

        req = None
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
                req = Request(method, path, query, self.headers, body, kwargs)
                req.load_session()
                result = handler(conn, req, **kwargs)
                self._send_result(result, req)
                # Never leave a transaction open on the thread connection:
                # SQLite allows one writer, and a stray open transaction would
                # block every other thread.
                conn.commit()
                return
            if method == "HEAD":
                self._send(404, "text/plain; charset=utf-8", "")
            else:
                if req is None:
                    req = Request(method, path, query, self.headers, body, {})
                    req.load_session()
                self._send_result(views.not_found(conn, req), req)
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            # The error page must never itself fail: if rendering the 500
            # page blows up, send plain text instead of dying silently,
            # which would leave the socket open and the browser hanging.
            try:
                self._send_result(views.not_found(conn, req, code=500,
                                                  message="The shop hit a snag."),
                                  req)
            except Exception:
                try:
                    self._send(500, "text/plain; charset=utf-8",
                               "The shop hit a snag.\n")
                except Exception:
                    pass
            # The error page itself may be what broke, so never let the
            # fallback raise: a plain body always beats a hung socket.
            try:
                self._send_result(views.not_found(conn, req, code=500,
                                                  message="The shop hit a snag."),
                                  req)
            except Exception:
                traceback.print_exc()
                try:
                    self._send(500, "text/plain; charset=utf-8",
                               "500 - the shop hit a snag. Please try again.")
                except Exception:
                    pass
            finally:
                try:
                    self.close_connection = True
                except Exception:
                    pass

    # -- responses --------------------------------------------------------
    def _send_result(self, result, req: Request) -> None:
        extra: dict[str, str] = {}
        content_type = "text/html; charset=utf-8"
        status = 200
        body: object = result
        if isinstance(result, tuple):
            if len(result) == 3:
                status, headers, body = result
                if isinstance(headers, dict):
                    extra = dict(headers)
                    content_type = "text/plain; charset=utf-8"
                else:
                    content_type = headers
            elif len(result) == 2:
                status, body = result
        cookies = list(req.set_cookies) if req is not None else []
        for cookie in cookies:
            extra.setdefault("Set-Cookie", cookie)
        if "Set-Cookie" in extra and len(cookies) > 1:
            # Multiple cookies need one header each.
            extra.pop("Set-Cookie")
            self._send(status, content_type, body, extra=extra,
                       cookies=cookies)
            return
        self._send(status, content_type, body, extra=extra)

    def _send(self, status: int, content_type: str, body, extra=None,
              cookies=None) -> None:
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
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        for cookie in (cookies or []):
            self.send_header("Set-Cookie", cookie)
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
        if content_type in ("font/woff2", "font/woff", "application/font-woff2"):
            content_type = "font/woff2"
        cache = "public, max-age=604800" if target.suffix not in (".html",) else "no-cache"
        self._send(200, content_type, target.read_bytes(),
                   extra={"Cache-Control": cache})


# --------------------------------------------------------------------------
# route table
# --------------------------------------------------------------------------
def register_routes() -> None:
    ROUTES.clear()
    views.register(ROUTES)


# --------------------------------------------------------------------------
# server
# --------------------------------------------------------------------------
class ShopServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 64


def build_server(host: str = config.DEFAULT_HOST, port: int = config.DEFAULT_PORT,
                 quiet: bool = False) -> ShopServer:
    config.ensure_dirs()
    register_routes()
    conn = db.connect()
    db.init_db(conn)
    conn.close()
    return ShopServer((host, port), ShopHandler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runchero Beef shop")
    parser.add_argument("--host", default=config.DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=config.DEFAULT_PORT)
    parser.add_argument("--seed", action="store_true",
                        help="seed the database before serving")
    parser.add_argument("--seed-only", action="store_true",
                        help="seed the database and exit without serving")
    args = parser.parse_args(argv)

    if args.seed or args.seed_only:
        from .seed.run import seed
        config.ensure_dirs()
        conn = db.connect()
        db.init_db(conn)
        conn.close()
        with db.session() as conn:
            report = seed(conn)
        print(f"seeded: {report}", flush=True)
        if args.seed_only:
            return 0

    try:
        server = build_server(args.host, args.port)
    except OSError as exc:
        print(f"cannot bind {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1

    # Write the pid after the bind succeeds so a stop never targets a process
    # that failed to start.
    try:
        config.PID_PATH.parent.mkdir(parents=True, exist_ok=True)
        config.PID_PATH.write_text(f"{os.getpid()}\n")
    except OSError:
        pass

    def shutdown(*_):
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    print(f"{config.SITE_NAME} listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
    return 0
