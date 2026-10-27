"""Turn Amazon product and search links into tagged affiliate links.

The rules are deliberately conservative: only Amazon US hosts are accepted,
the product ID is validated, tracking parameters are removed, and the
affiliate tag is added last. Nothing is shortened, cloaked, or redirected.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

AMAZON_BASE_HOST = "amazon.com"
AMAZON_HOSTS = {
    "amazon.com",
    "www.amazon.com",
    "m.amazon.com",
    "smile.amazon.com",
}
SHORT_HOSTS = {"a.co", "amzn.to", "amzn.com"}

TRACKING_PARAMS = {
    "tag",
    "linkcode",
    "linkid",
    "ref",
    "ref_",
    "th",
    "psc",
    "social_share",
    "sprefix",
    "crid",
    "qid",
    "content-id",
    "smid",
    "spia",
    "ps",
    "_encoding",
    "language",
    "currency",
}

TRACKING_PREFIXES = ("pf_rd_", "pd_rd_")

KEPT_SEARCH_PARAMS = {"k", "i", "node", "rh", "field-keywords"}

ASIN_RE = re.compile(r"^[A-Za-z0-9]{10}$")
PRODUCT_RE = re.compile(
    r"/(?:dp|gp/product|gp/aw/d|gp/aw/product)/([A-Za-z0-9]{10})(?:/|$)",
    re.IGNORECASE,
)
NAME_DP_RE = re.compile(
    r"/[^/]+/(?:dp|gp/product|gp/aw/d)/([A-Za-z0-9]{10})(?:/|$)",
    re.IGNORECASE,
)
SEARCH_PATHS = {"/s", "/gp/search", "/gp/aw/s"}


@dataclass
class Conversion:
    ok: bool
    original: str
    affiliate_url: str = ""
    kind: str = ""
    asin: str = ""
    keywords: str = ""
    note: str = ""
    error: str = ""

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "original": self.original,
            "affiliate_url": self.affiliate_url,
            "kind": self.kind,
            "asin": self.asin,
            "keywords": self.keywords,
            "note": self.note,
            "error": self.error,
        }


def normalise_host(host: str) -> str:
    return (host or "").strip().lower().rstrip(".")


def is_amazon_host(host: str) -> bool:
    host = normalise_host(host)
    if host in AMAZON_HOSTS:
        return True
    return host.endswith("." + AMAZON_BASE_HOST)


def is_short_host(host: str) -> bool:
    return normalise_host(host) in SHORT_HOSTS


def is_tracking_param(name: str) -> bool:
    lowered = name.lower()
    return lowered in TRACKING_PARAMS or lowered.startswith(TRACKING_PREFIXES)


def clean_query(pairs, keep_only=None):
    seen = set()
    kept = []
    for name, value in pairs:
        lowered = name.lower()
        if keep_only is not None and lowered not in keep_only:
            continue
        if is_tracking_param(name):
            continue
        if lowered in seen:
            continue
        seen.add(lowered)
        kept.append((name, value))
    return kept


def _build(scheme: str, netloc: str, path: str, query) -> str:
    encoded = urlencode(query, doseq=False, quote_via=quote)
    return urlunsplit((scheme, netloc, path, encoded, ""))


def _error(original: str, message: str, kind: str = "") -> Conversion:
    return Conversion(ok=False, original=original, error=message, kind=kind)


def _validate_url(raw: str) -> tuple[Conversion | None, object]:
    text = (raw or "").strip()
    if not text:
        return _error(raw, "Paste an Amazon link first."), None
    if len(text) > 2000:
        return _error(raw, "That link is too long to convert."), None
    try:
        parts = urlsplit(text)
    except ValueError:
        return _error(raw, "That does not look like a web address."), None
    if parts.scheme.lower() not in ("http", "https"):
        return _error(raw, "Only http and https links are accepted."), None
    if parts.username or parts.password:
        return _error(raw, "Links with a username or password are not accepted."), None
    host = normalise_host(parts.hostname or "")
    if not host:
        return _error(raw, "That link is missing a website address."), None
    try:
        port = parts.port
    except ValueError:
        return _error(raw, "That link has an invalid port."), None
    if port not in (None, 80, 443):
        return _error(raw, "That link uses an unexpected port."), None
    return None, parts


def convert(
    raw: str,
    tag: str,
    allow_short: bool = True,
    resolver=None,
) -> Conversion:
    early, parts = _validate_url(raw)
    if early is not None:
        return early

    host = normalise_host(parts.hostname or "")
    if is_short_host(host):
        if not allow_short:
            return _error(
                raw,
                "Short links like a.co or amzn.to need to be resolved first.",
                kind="short",
            )
        if resolver is None:
            return _error(raw, "That short link cannot be resolved right now.", kind="short")
        try:
            resolved = resolver(raw)
        except Exception as exc:
            message = str(exc) or "The short link could not be resolved."
            return _error(raw, message, kind="short")
        result = convert(resolved, tag, allow_short=False)
        result.original = raw
        result.note = result.note or "Resolved from a short link."
        return result

    if not is_amazon_host(host):
        return _error(
            raw,
            "Only Amazon links are converted. Paste an amazon.com product or search link.",
        )

    scheme = "https"
    netloc = "www.amazon.com" if host == AMAZON_BASE_HOST else host
    path = parts.path or "/"
    pairs = parse_qsl(parts.query, keep_blank_values=True)

    match = PRODUCT_RE.search(path) or NAME_DP_RE.search(path)
    if match:
        asin = match.group(1)
        if not ASIN_RE.match(asin):
            return _error(raw, "That product ID does not look valid.")
        url = _build(scheme, netloc, f"/dp/{asin}", [("tag", tag)])
        return Conversion(
            ok=True,
            original=raw,
            affiliate_url=url,
            kind="product",
            asin=asin,
        )
    lowered_path = path.lower()
    if "/dp/" in lowered_path or "/gp/product/" in lowered_path or "/gp/aw/d/" in lowered_path:
        return _error(raw, "That product ID does not look valid. It must be 10 letters or numbers.")

    keywords = ""
    for name, value in pairs:
        if name.lower() in ("k", "field-keywords"):
            keywords = value.strip()
            break

    if (path.rstrip("/").lower() in SEARCH_PATHS) or keywords:
        kept = clean_query(pairs, KEPT_SEARCH_PARAMS)
        if keywords:
            kept = [(n, v) for n, v in kept if n.lower() not in ("k", "field-keywords")]
            kept.insert(0, ("k", keywords))
        if not any(n.lower() in ("k", "field-keywords") for n, _ in kept):
            return _error(raw, "That search link is missing what to search for.")
        kept.append(("tag", tag))
        url = _build(scheme, netloc, "/s", kept)
        return Conversion(
            ok=True,
            original=raw,
            affiliate_url=url,
            kind="search",
            keywords=keywords,
        )

    kept = clean_query(pairs)
    kept.append(("tag", tag))
    url = _build(scheme, netloc, path, kept)
    return Conversion(
        ok=True,
        original=raw,
        affiliate_url=url,
        kind="page",
        note="This is an Amazon page, not a product or search. The tag was still added.",
    )


def convert_many(raw_text: str, tag: str, allow_short: bool = True,
                 resolver=None, limit: int = 50):
    lines = []
    for line in (raw_text or "").splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    total = len(lines)
    lines = lines[:limit]
    results = [
        convert(line, tag, allow_short=allow_short, resolver=resolver)
        for line in lines
    ]
    return results, total


def build_search_url(keywords: str, tag: str, base: str = "https://www.amazon.com") -> str:
    text = " ".join((keywords or "").split())
    if not text:
        raise ValueError("Type what you want to search for.")
    if len(text) > 200:
        raise ValueError("That search is too long.")
    return f"{base}/s?{urlencode([('k', text), ('tag', tag)], quote_via=quote)}"
