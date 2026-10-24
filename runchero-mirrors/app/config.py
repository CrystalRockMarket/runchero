"""Configuration for Runchero Mirrors.

Every path can be overridden with an environment variable so the app can run
on the farm box, a laptop, or a different shared server without code changes.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

SITE_NAME = os.environ.get("RMM_SITE_NAME", "Runchero Mirrors")
SITE_SHORT = os.environ.get("RMM_SITE_SHORT", "Mirrors")
SITE_TAGLINE = os.environ.get(
    "RMM_SITE_TAGLINE", "Save the websites our community relies on."
)
SITE_BADGE = os.environ.get("RMM_BADGE", "COMMUNITY DEPOT")
SITE_VERSION = "0.3.0"

DATA_DIR = Path(os.environ.get("RMM_DATA_DIR", "/home/barn/data")).resolve()
DB_PATH = Path(os.environ.get("RMM_DB_PATH", str(DATA_DIR / "runchero-mirrors.db")))

MIRRORS_ROOT = Path(
    os.environ.get("RMM_MIRRORS_ROOT", "/home/barn/mirrors")
).resolve()
ARCHIVE_DIR = MIRRORS_ROOT

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

DEFAULT_HOST = os.environ.get("RMM_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RMM_PORT", "8090"))

RUN_DIR = Path(os.environ.get("RMM_RUN_DIR", "/home/barn/run")).resolve()
LOG_DIR = Path(os.environ.get("RMM_LOG_DIR", "/home/barn/logs")).resolve()
PID_PATH = Path(os.environ.get("RMM_PID_PATH", str(RUN_DIR / "runchero-mirrors.pid")))
LOG_PATH = Path(os.environ.get("RMM_LOG_PATH", str(LOG_DIR / "runchero-mirrors.log")))

#: HTTrack is vendored with the app so the archive keeps working after a reboot.
#: An administrator can override the binary with RMM_HTTRACK_BIN.
_VENDORED_HTTRACK = PROJECT_DIR / "vendor" / "httrack" / "usr" / "bin" / "httrack"
_VENDORED_LIB = PROJECT_DIR / "vendor" / "httrack" / "usr" / "lib" / "x86_64-linux-gnu"
HTTRACK_BIN = os.environ.get(
    "RMM_HTTRACK_BIN",
    str(_VENDORED_HTTRACK) if _VENDORED_HTTRACK.exists() else (shutil.which("httrack") or "httrack"),
)
HTTRACK_LIB = os.environ.get(
    "RMM_HTTRACK_LIB",
    str(_VENDORED_LIB) if _VENDORED_LIB.exists() else "",
)

#: One active crawl at a time keeps the box and the remote sites happy.
MAX_CONCURRENT = max(1, int(os.environ.get("RMM_MAX_CONCURRENT", "1")))
MAX_QUEUE = max(1, int(os.environ.get("RMM_MAX_QUEUE", "20")))

#: Bytes per second, depth and total limits for each speed choice. The defaults
#: are deliberately polite: the default is roughly a few pages per minute.
CRAWL_PROFILES: dict[str, dict[str, object]] = {
    "very-slow": {
        "label": "Very slow",
        "description": "Safest for most sites: roughly 2-5 pages per minute.",
        "rate": 12000,
        "depth": 4,
        "sockets": 1,
        "max_bytes": 750_000_000,
        "max_seconds": 12 * 60 * 60,
    },
    "slow": {
        "label": "Slow",
        "description": "A gentle pace: roughly 5-10 pages per minute.",
        "rate": 24000,
        "depth": 5,
        "sockets": 1,
        "max_bytes": 1_000_000_000,
        "max_seconds": 12 * 60 * 60,
    },
    "medium": {
        "label": "Medium",
        "description": "Faster, but still one connection: roughly 10-25 pages per minute.",
        "rate": 50000,
        "depth": 6,
        "sockets": 2,
        "max_bytes": 1_500_000_000,
        "max_seconds": 10 * 60 * 60,
    },
}
DEFAULT_SPEED = os.environ.get("RMM_DEFAULT_SPEED", "very-slow")
if DEFAULT_SPEED not in CRAWL_PROFILES:
    DEFAULT_SPEED = "very-slow"

#: Set to 1 only on a trusted network to allow mirroring private/local hosts.
ALLOW_PRIVATE_HOSTS = os.environ.get("RMM_ALLOW_PRIVATE_HOSTS", "0") in (
    "1", "true", "yes",
)

USER_AGENT = os.environ.get(
    "RMM_USER_AGENT",
    "RuncheroMirrors/0.2 (community offline archive; contact: osborne@runchero.example)",
)

MAX_REQUEST_BYTES = 2 * 1024 * 1024
SECRET_KEY = os.environ.get("RMM_SECRET_KEY", "")


def ensure_dirs() -> None:
    for path in (
        DATA_DIR,
        MIRRORS_ROOT,
        MIRRORS_ROOT / ".cache",
        RUN_DIR,
        LOG_DIR,
        STATIC_DIR / "css",
        STATIC_DIR / "js",
        STATIC_DIR / "img" / "icons",
        STATIC_DIR / "fonts",
    ):
        path.mkdir(parents=True, exist_ok=True)


def profile(speed: str) -> dict[str, object]:
    return CRAWL_PROFILES.get(speed, CRAWL_PROFILES[DEFAULT_SPEED])
