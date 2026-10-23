"""HTTP server for Runchero Mirrors."""
from __future__ import annotations

import argparse
import mimetypes
import os
import re
import signal
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import config, db, views
from .web import Request

ROUTES: list[tuple[str, re.Pattern[str], object]] = []
STATIC_ROOT = config.STATIC_DIR.resolve()
_THREAD_LOCAL = threading.local()


def route(pattern: str, method: str = "GET"):
    compiled = re.compile(pattern)

    def decorator(func):
        ROUTES.append((method, compiled, func))
        return func
    return decorator


def _local():
    conn = getattr(_THREAD_LOCAL, "conn", None)
    if conn is None:
        conn = db.connect()
        _THREAD_LOCAL.conn = conn
    return conn


class MirrorHandler(BaseHTTPRequestHandler):
    server_version = f"RuncheroMirrors/{config.SITE_VERSION}"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write(f"[mirrors] {self.address_string()} {fmt % args}\n")

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_HEAD(self) -> None:
        self._dispatch("HEAD")

    def do_POST(self) -> None:
        self._dispatch("POST")

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
        if method in ("POST",):
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
                try:
                    conn.commit()
                except Exception:
                    pass
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
            try:
                if req is None:
                    req = Request(method, path, query, self.headers, body, {})
                    req.load_session()
                self._send_result(views.server_error(conn, req), req)
            except Exception:
                try:
                    self._send(500, "text/plain; charset=utf-8", "Server error\n")
                except Exception:
                    pass

    def _send_result(self, result, req: Request) -> None:
        extra = {}
        content_type = "text/html; charset=utf-8"
        status = 200
        body = result
        if isinstance(result, tuple):
            if len(result) == 3:
                status, headers, body = result
                if isinstance(headers, dict):
                    extra = dict(headers)
                else:
                    content_type = headers
            elif len(result) == 2:
                status, body = result
        cookies = list(req.set_cookies) if req is not None else []
        if "Set-Cookie" in extra and len(cookies) > 1:
            extra.pop("Set-Cookie")
            self._send(status, content_type, body, extra=extra, cookies=cookies)
            return
        self._send(status, content_type, body, extra=extra)

    def _send(self, status: int, content_type: str, body, extra=None, cookies=None) -> None:
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
        self.send_header("X-Frame-Options", "SAMEORIGIN")
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
        if content_type.startswith("text/") or content_type in ("application/javascript", "application/json", "application/manifest+json"):
            content_type += "; charset=utf-8"
        cache = "public, max-age=604800" if target.suffix not in (".html",) else "no-cache"
        self._send(200, content_type, target.read_bytes(), extra={"Cache-Control": cache})


class MirrorServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 64


def register_routes() -> None:
    ROUTES.clear()
    views.register(ROUTES)


def build_server(host: str = config.DEFAULT_HOST, port: int = config.DEFAULT_PORT) -> MirrorServer:
    config.ensure_dirs()
    register_routes()
    conn = db.connect()
    db.init_db(conn)
    conn.close()
    return MirrorServer((host, port), MirrorHandler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runchero Mirrors")
    parser.add_argument("--host", default=config.DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=config.DEFAULT_PORT)
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--seed-only", action="store_true")
    args = parser.parse_args(argv)

    if args.seed or args.seed_only:
        config.ensure_dirs()
        conn = db.connect()
        db.init_db(conn)
        conn.close()
        print("initialized database and directories", flush=True)
        if args.seed_only:
            return 0

    try:
        server = build_server(args.host, args.port)
    except OSError as exc:
        print(f"cannot bind {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1

    try:
        config.PID_PATH.parent.mkdir(parents=True, exist_ok=True)
        config.PID_PATH.write_text(f"{os.getpid()}\n")
    except Exception:
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
        try:
            if config.PID_PATH.exists():
                config.PID_PATH.unlink()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
