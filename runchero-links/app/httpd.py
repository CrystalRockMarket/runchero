"""Small standard-library HTTP server for Runchero Links."""
from __future__ import annotations

import argparse
import mimetypes
import os
import re
import signal
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import config, views, web

STATIC_ROOT = config.STATIC_DIR.resolve()

ROUTES = [
    ("GET", re.compile(r"^/$"), views.home),
    ("GET", re.compile(r"^/convert$"), views.home),
    ("POST", re.compile(r"^/convert$"), views.convert),
    ("GET", re.compile(r"^/api/convert$"), views.api_convert),
    ("POST", re.compile(r"^/api/convert$"), views.api_convert),
    ("GET", re.compile(r"^/api/search$"), views.api_search),
    ("GET", re.compile(r"^/how$"), views.how),
    ("GET", re.compile(r"^/healthz$"), views.health),
]

CSP = (
    "default-src 'self'; "
    "base-uri 'none'; "
    "frame-ancestors 'none'; "
    "form-action 'self' https://www.amazon.com; "
    "img-src 'self' data:; "
    "style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "object-src 'none'"
)


class Handler(BaseHTTPRequestHandler):
    server_version = f"RuncheroLinks/{config.SITE_VERSION}"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:
        path = (urlparse(self.path).path or "/")
        sys.stderr.write(f"[links] {self.address_string()} {self.command} {path} {fmt % args}\n")

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_HEAD(self) -> None:
        self._dispatch("HEAD")

    def do_POST(self) -> None:
        self._dispatch("POST")

    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path) or "/"
        if len(path) > 1 and path.endswith("/") and not path.startswith("/static/"):
            path = path.rstrip("/") or "/"
        query = {key: ",".join(values) for key, values in parse_qs(parsed.query).items()}

        if path.startswith("/static/"):
            self._serve_static(path[len("/static/"):])
            return

        body = b""
        if method == "POST":
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                length = 0
            length = max(0, min(length, config.MAX_REQUEST_BYTES))
            if length:
                body = self.rfile.read(length)

        req = web.Request(
            method,
            path,
            query,
            self.headers,
            body,
            client_ip=self.client_address[0] if self.client_address else "",
        )
        try:
            for verb, pattern, handler in ROUTES:
                if verb != method and not (verb == "GET" and method == "HEAD"):
                    continue
                if not pattern.match(path):
                    continue
                self._send_result(handler(req), req)
                return
            self._send_result(views.not_found(req), req)
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            try:
                self._send_result(views.server_error(req), req)
            except Exception:
                self._send(500, "text/plain; charset=utf-8", "Server error\n")

    def _send_result(self, result, req: web.Request) -> None:
        status = 200
        content_type = "text/html; charset=utf-8"
        extra: dict[str, str] = {}
        body = result
        if isinstance(result, tuple):
            if len(result) == 3:
                status, headers, body = result
                if isinstance(headers, dict):
                    extra = dict(headers)
                    content_type = extra.pop("Content-Type", content_type)
                else:
                    content_type = headers
            elif len(result) == 2:
                status, body = result
        if ("Cache-Control" not in extra
                and (content_type.startswith("text/html")
                     or content_type.startswith("application/json"))):
            extra["Cache-Control"] = "no-store"
        self._send(status, content_type, body, extra=extra)

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
        self._security_headers()
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _security_headers(self) -> None:
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")

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
        ):
            content_type += "; charset=utf-8"
        cache = "public, max-age=604800"
        self._send(200, content_type, target.read_bytes(), extra={"Cache-Control": cache})


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 64


def build_server(host: str = config.DEFAULT_HOST, port: int = config.DEFAULT_PORT) -> Server:
    return Server((host, port), Handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=config.SITE_NAME)
    parser.add_argument("--host", default=config.DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=config.DEFAULT_PORT)
    args = parser.parse_args(argv)

    try:
        server = build_server(args.host, args.port)
    except OSError as exc:
        print(f"cannot bind {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1

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
        try:
            if config.PID_PATH.exists():
                config.PID_PATH.unlink()
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
