"""Tiny in-memory rate limiter for anonymous forms and admin logins."""
from __future__ import annotations

import threading
import time

_lock = threading.Lock()
_hits: dict[str, list[float]] = {}


def allow(key: str, limit: int, window: float) -> bool:
    now = time.monotonic()
    with _lock:
        bucket = [stamp for stamp in _hits.get(key, []) if now - stamp < window]
        if len(bucket) >= limit:
            _hits[key] = bucket
            return False
        bucket.append(now)
        _hits[key] = bucket
        if len(_hits) > 5000:
            for old in [name for name, stamps in _hits.items() if not stamps]:
                _hits.pop(old, None)
    return True
