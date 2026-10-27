"""Jinja environment, signed cookies, CSRF, and the request object."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from datetime import datetime
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

_env: Environment | None = None
_SECRET: bytes | None = None


def secret() -> bytes:
    global _SECRET
    if _SECRET:
        return _SECRET
    if config.SECRET_KEY:
        _SECRET = config.SECRET_KEY.encode("utf-8")
        return _SECRET
    path = config.DATA_DIR / ".runchero-community-secret"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            raw = path.read_text(encoding="ascii").strip()
            if len(raw) >= 32:
                _SECRET = raw.encode("ascii")
                return _SECRET
        raw = secrets.token_hex(32)
        path.write_text(raw, encoding="ascii")
        try:
            path.chmod(0o600)
        except OSError:
            pass
        _SECRET = raw.encode("ascii")
    except OSError:
        _SECRET = secrets.token_bytes(32)
    return _SECRET


def _sign(payload: bytes) -> str:
    return hmac.new(secret(), payload, hashlib.sha256).hexdigest()[:32]


def sign_value(value) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    blob = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"{blob}.{_sign(raw)}"


def unsign_value(token: str):
    if not token or "." not in token:
        return None
    blob, _, signature = token.rpartition(".")
    padding = "=" * (-len(blob) % 4)
    try:
        raw = base64.urlsafe_b64decode(blob + padding)
    except (ValueError, TypeError):
        return None
    if not hmac.compare_digest(_sign(raw), signature):
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None


def _date(value: str) -> str:
    try:
        moment = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return value or ""
    return moment.strftime("%b %d, %Y · %I:%M %p").replace(" 0", " ")


def environment() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        _env.filters["dt"] = _date
        _env.globals.update(
            site_name=config.SITE_NAME,
            site_short=config.SITE_SHORT,
            site_tagline=config.SITE_TAGLINE,
            site_badge=config.SITE_BADGE,
            site_version=config.SITE_VERSION,
            kinds=config.KINDS,
            kind_icons=config.KIND_ICONS,
            categories=config.CATEGORIES,
            admin_user=config.ADMIN_USER,
            max_name=config.MAX_NAME,
            max_description=config.MAX_DESCRIPTION,
            max_location=config.MAX_LOCATION,
            max_submitter=config.MAX_SUBMITTER,
            max_channel_label=config.MAX_CHANNEL_LABEL,
            max_channel_value=config.MAX_CHANNEL_VALUE,
            max_admin_note=config.MAX_ADMIN_NOTE,
            max_custom=config.MAX_CUSTOM,
        )
    return _env


def render(template: str, **context) -> str:
    return environment().get_template(template).render(**context)


class Request:
    def __init__(self, method: str, path: str, query: dict[str, str], headers,
                 body: bytes = b"", client_ip: str = ""):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
        self.client_ip = client_ip
        self.set_cookies: list[str] = []
        self._form: dict[str, str] | None = None
        self._json = None
        self._json_done = False
        self._cookies: dict[str, str] | None = None

    @property
    def form(self) -> dict[str, str]:
        if self._form is None:
            self._form = {}
            if self.body:
                text = self.body.decode("utf-8", "replace")
                for key, values in parse_qs(text, keep_blank_values=True).items():
                    self._form[key] = values[-1]
        return self._form

    @property
    def json_body(self):
        if not self._json_done:
            self._json_done = True
            if self.body:
                try:
                    self._json = json.loads(self.body.decode("utf-8"))
                except (ValueError, UnicodeDecodeError):
                    self._json = None
        return self._json

    @property
    def cookies(self) -> dict[str, str]:
        if self._cookies is None:
            jar = SimpleCookie()
            try:
                jar.load(self.headers.get("Cookie") or "")
            except Exception:
                self._cookies = {}
            else:
                self._cookies = {key: morsel.value for key, morsel in jar.items()}
        return self._cookies

    def cookie(self, name: str) -> str:
        return self.cookies.get(name, "")

    def set_cookie(self, name: str, value: str, max_age: int = 3600,
                   http_only: bool = True) -> None:
        parts = [f"{name}={value}", "Path=/", f"Max-Age={max_age}", "SameSite=Lax"]
        if http_only:
            parts.append("HttpOnly")
        if config.SECURE_COOKIES:
            parts.append("Secure")
        cookie = "; ".join(parts)
        for index, existing in enumerate(self.set_cookies):
            if existing.startswith(f"{name}="):
                self.set_cookies[index] = cookie
                return
        self.set_cookies.append(cookie)

    def clear_cookie(self, name: str) -> None:
        blank = f"{name}=; Path=/; Max-Age=0; SameSite=Lax; HttpOnly"
        for index, existing in enumerate(self.set_cookies):
            if existing.startswith(f"{name}="):
                self.set_cookies[index] = blank
                return
        self.set_cookies.append(blank)

    def csrf_token(self) -> str:
        token = self.cookie(config.CSRF_COOKIE)
        if not token or len(token) < 20:
            token = secrets.token_urlsafe(24)
        self.set_cookie(config.CSRF_COOKIE, token, max_age=config.SESSION_MAX_AGE,
                        http_only=False)
        return token

    def csrf_ok(self) -> bool:
        sent = self.form.get("_csrf") or ""
        stored = self.cookie(config.CSRF_COOKIE)
        return bool(sent and stored) and hmac.compare_digest(sent, stored)

    def admin_logged_in(self) -> bool:
        data = unsign_value(self.cookie(config.ADMIN_COOKIE))
        if not isinstance(data, dict):
            return False
        if not data.get("admin"):
            return False
        if data.get("user") != config.ADMIN_USER:
            return False
        try:
            expires = float(data.get("exp") or 0)
        except (TypeError, ValueError):
            return False
        return expires > time.time()

    def login_admin(self) -> None:
        token = sign_value({
            "admin": True,
            "user": config.ADMIN_USER,
            "exp": time.time() + config.SESSION_MAX_AGE,
        })
        self.set_cookie(config.ADMIN_COOKIE, token, max_age=config.SESSION_MAX_AGE)

    def logout_admin(self) -> None:
        self.clear_cookie(config.ADMIN_COOKIE)
