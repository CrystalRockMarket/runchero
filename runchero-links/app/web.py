"""Jinja environment and a small request object."""
from __future__ import annotations

import json
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

_env: Environment | None = None


def environment() -> Environment:
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
            affiliate_tag=config.AFFILIATE_TAG,
            amazon_site=config.AMAZON_SITE,
            disclosure=config.DISCLOSURE,
            example_searches=config.EXAMPLE_SEARCHES,
            example_prices=config.EXAMPLE_PRICES,
            default_rate=config.DEFAULT_COMMISSION_RATE,
            min_rate=config.MIN_COMMISSION_RATE,
            max_rate=config.MAX_COMMISSION_RATE,
        )
        _env.filters["money"] = _money
    return _env


def _money(value) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "$0.00"
    return f"${number:,.2f}"


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
        self._form: dict[str, str] | None = None
        self._json = None
        self._json_done = False

    @property
    def form(self) -> dict[str, str]:
        if self._form is None:
            self._form = {}
            if self.body:
                ctype = (self.headers.get("Content-Type") or "").lower()
                if "application/json" in ctype:
                    return self._form
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

    def input_value(self, name: str) -> str:
        value = self.form.get(name)
        if value is None:
            value = self.query.get(name, "")
        return value or ""
