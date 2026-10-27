"""Resolve a.co and amzn.to shortcuts into the Amazon page they point at.

Only Amazon-owned hosts are followed. Each redirect hop is checked, the
number of hops is capped, and the whole request has a short timeout so a
bad shortcut cannot tie up the server or reach an internal address.
"""
from __future__ import annotations

import threading
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

from .amazon import is_amazon_host, is_short_host

USER_AGENT = "RuncheroLinks/0.1 (+community link tool)"


class ResolveError(Exception):
    pass


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, max_redirects: int):
        self.max_redirects = max_redirects
        self.count = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.count += 1
        if self.count > self.max_redirects:
            raise ResolveError("That shortcut redirects too many times.")
        host = (urlsplit(newurl).hostname or "").lower()
        if not (is_short_host(host) or is_amazon_host(host)):
            raise ResolveError("That shortcut points to a site that is not Amazon.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def resolve_short(url: str, timeout: float = 5.0, max_redirects: int = 5) -> str:
    host = (urlsplit(url).hostname or "").lower()
    if not is_short_host(host):
        raise ResolveError("Only a.co and amzn.to shortcuts can be resolved.")
    opener = urllib.request.build_opener(_SafeRedirect(max_redirects))
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    final = ""
    try:
        with opener.open(request, timeout=timeout) as response:
            final = response.geturl()
    except urllib.error.HTTPError as exc:
        final = getattr(exc, "url", "") or ""
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ResolveError(
            "The shortcut service could not be reached. Paste the full Amazon link instead."
        ) from None
    if not final:
        raise ResolveError("That shortcut did not lead anywhere. Paste the full Amazon link.")
    final_host = (urlsplit(final).hostname or "").lower()
    if not is_amazon_host(final_host):
        raise ResolveError("That shortcut did not lead to an Amazon page.")
    return final


_lock = threading.Lock()
_hits: dict[str, list[float]] = {}


def check_rate(key: str, limit: int = 30, window: float = 60.0) -> bool:
    now = time.monotonic()
    with _lock:
        bucket = [stamp for stamp in _hits.get(key, []) if now - stamp < window]
        if len(bucket) >= limit:
            _hits[key] = bucket
            return False
        bucket.append(now)
        _hits[key] = bucket
        if len(_hits) > 2000:
            for old_key in [k for k, v in _hits.items() if not v]:
                _hits.pop(old_key, None)
    return True
