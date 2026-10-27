"""Page and API handlers."""
from __future__ import annotations

import json

from . import config, web
from .services import amazon, resolve


def _ctx(req: web.Request, **extra) -> dict:
    context = {
        "path": req.path,
        "prefill": "",
        "results": [],
        "total_lines": 0,
        "too_many": False,
        "submitted": False,
        "search_error": "",
        "max_bulk": config.MAX_BULK_LINKS,
        "max_keywords": config.MAX_KEYWORDS_LENGTH,
        "max_url": config.MAX_URL_LENGTH,
    }
    context.update(extra)
    return context


def _json(payload, status: int = 200):
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    return status, "application/json; charset=utf-8", body


def _resolver_for(req: web.Request):
    def run(url: str) -> str:
        if not resolve.check_rate(req.client_ip, config.RESOLVE_MATCHES_PER_MINUTE):
            raise resolve.ResolveError(
                "Too many short links from this device. Wait a minute and try again."
            )
        return resolve.resolve_short(
            url,
            timeout=config.RESOLVE_TIMEOUT,
            max_redirects=config.RESOLVE_MAX_REDIRECTS,
        )

    return run


def _input_text(req: web.Request) -> str:
    data = req.json_body
    if isinstance(data, dict):
        value = data.get("urls")
        if value is None:
            value = data.get("url")
        if isinstance(value, list):
            return "\n".join(str(item) for item in value)
        if value is not None:
            return str(value)
    return req.input_value("urls") or req.input_value("url")


def _wants_json(req: web.Request) -> bool:
    if req.path.startswith("/api/"):
        return True
    if req.query.get("format", "").lower() == "json":
        return True
    return "application/json" in (req.headers.get("Accept") or "").lower()


def home(req: web.Request, **_):
    prefill = " ".join((req.query.get("q") or "").split())[: config.MAX_KEYWORDS_LENGTH]
    return 200, "text/html; charset=utf-8", web.render("home.html", **_ctx(req, prefill=prefill))


def convert(req: web.Request, **_):
    text = _input_text(req)
    resolver = _resolver_for(req) if req.client_ip else None
    results, total = amazon.convert_many(
        text,
        config.AFFILIATE_TAG,
        allow_short=True,
        resolver=resolver,
        limit=config.MAX_BULK_LINKS,
    )
    payload = {
        "tag": config.AFFILIATE_TAG,
        "total": total,
        "converted": sum(1 for item in results if item.ok),
        "failed": sum(1 for item in results if not item.ok),
        "results": [item.as_dict() for item in results],
    }
    if _wants_json(req):
        return _json(payload)
    return 200, "text/html; charset=utf-8", web.render(
        "results.html",
        **_ctx(
            req,
            results=results,
            total_lines=total,
            too_many=total > config.MAX_BULK_LINKS,
            submitted=True,
        ),
    )


def api_convert(req: web.Request, **_):
    return convert(req)


def api_search(req: web.Request, **_):
    keywords = " ".join((req.query.get("q") or "").split())
    try:
        url = amazon.build_search_url(keywords, config.AFFILIATE_TAG)
    except ValueError as exc:
        return _json({"ok": False, "error": str(exc)}, status=400)
    return _json({"ok": True, "keywords": keywords, "affiliate_url": url})


def how(req: web.Request, **_):
    return 200, "text/html; charset=utf-8", web.render("how.html", **_ctx(req))


def health(req: web.Request, **_):
    return _json({"ok": True, "service": config.SITE_NAME, "version": config.SITE_VERSION,
                  "tag": config.AFFILIATE_TAG})


def not_found(req: web.Request, **_):
    body = web.render("error.html", **_ctx(req, code=404, message="That page does not exist."))
    return 404, "text/html; charset=utf-8", body


def server_error(req: web.Request, **_):
    body = web.render(
        "error.html",
        **_ctx(req, code=500, message="Something went wrong on our side. Try again."),
    )
    return 500, "text/html; charset=utf-8", body
