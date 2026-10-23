"""Jinja environment and request helpers."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
from http.cookies import SimpleCookie
from typing import Any
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

_env: Environment | None = None


def secret() -> bytes:
    global _SECRET
    try:
        return _SECRET
    except NameError:
        pass
    if config.SECRET_KEY:
        _SECRET = config.SECRET_KEY.encode("utf-8")
    else:
        _SECRET = secrets.token_bytes(32)
    return _SECRET


_SECRET: bytes = b""


def _sign(payload: bytes) -> str:
    return hmac.new(secret(), payload, hashlib.sha256).hexdigest()[:32]


def sign_value(value: Any) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    blob = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"{blob}.{_sign(raw)}"


def unsign_value(token: str) -> Any:
    if not token or "." not in token:
        return None
    blob, _, signature = token.rpartition(".")
    padding = "=" * (-len(blob) % 4)
    try:
        raw = base64.urlsafe_b64decode(blob + padding)
    except Exception:
        return None
    if not hmac.compare_digest(_sign(raw), signature):
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None


class Request:
    def __init__(self, method: str, path: str, query: dict[str, str],
                 headers, body: bytes, params: dict[str, str] | None = None):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
        self.params = params or {}
        self._form: dict[str, str] | None = None
        self.session: dict[str, Any] = {}
        self.set_cookies: list[str] = []

    @property
    def form(self) -> dict[str, str]:
        if self._form is None:
            self._form = {}
            if self.body:
                ctype = (self.headers.get("Content-Type") or "").lower()
                if "application/json" in ctype:
                    return self._form
                try:
                    text = self.body.decode("utf-8", "replace")
                except Exception:
                    return self._form
                for key, values in parse_qs(text, keep_blank_values=True).items():
                    self._form[key] = values[-1]
            return self._form
        return self._form

    @property
    def cookies(self) -> dict[str, str]:
        jar = SimpleCookie()
        try:
            jar.load(self.headers.get("Cookie") or "")
        except Exception:
            return {}
        return {key: morsel.value for key, morsel in jar.items()}

    def get_cookie(self, name: str) -> str | None:
        return self.cookies.get(name)

    def set_cookie(self, name: str, value: str, max_age: int = 60 * 60 * 24 * 7,
                   http_only: bool = True) -> None:
        parts = [f"{name}={value}", f"Path=/", f"Max-Age={max_age}", "SameSite=Lax"]
        if http_only:
            parts.append("HttpOnly")
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

    def load_session(self) -> None:
        raw = self.get_cookie("rmm_session")
        if raw:
            data = unsign_value(raw)
            if isinstance(data, dict):
                self.session = data

    def session_set(self, key: str, value: Any) -> None:
        self.session[key] = value
        if not self.session:
            self.clear_cookie("rmm_session")
            return
        self.set_cookie("rmm_session", sign_value(self.session))

    def session_pop(self, key: str, default: Any = None) -> Any:
        value = self.session.pop(key, default)
        if not self.session:
            self.clear_cookie("rmm_session")
        else:
            self.set_cookie("rmm_session", sign_value(self.session))
        return value

    def csrf_token(self) -> str:
        token = self.session.get("_csrf")
        if not token:
            token = secrets.token_urlsafe(24)
            self.session["_csrf"] = token
            self.set_cookie("rmm_session", sign_value(self.session))
        return token

    def csrf_ok(self) -> bool:
        sent = self.form.get("_csrf") or self.headers.get("X-CSRF-Token") or ""
        expected = self.session.get("_csrf") or ""
        return bool(expected) and hmac.compare_digest(expected, sent)


def env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        _env.globals.update(
            site_name=config.SITE_NAME,
            site_short=config.SITE_SHORT,
            site_tagline=config.SITE_TAGLINE,
            site_badge=config.SITE_BADGE,
            site_version=config.SITE_VERSION,
            static_url=lambda p: f"/static/{p.lstrip('/')}",
        )
    return _env


def render(template: str, **context: Any) -> str:
    return env().get_template(template).render(**context)
