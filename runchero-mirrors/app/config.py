"""Configuration for Runchero Mirrors."""
from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

SITE_NAME = os.environ.get("RMM_SITE_NAME", "Runchero Mirrors")
SITE_SHORT = os.environ.get("RMM_SITE_SHORT", "Mirrors")
SITE_TAGLINE = os.environ.get("RMM_SITE_TAGLINE", "Save community sites for offline browsing.")
SITE_BADGE = os.environ.get("RMM_BADGE", "COMMUNITY DEPOT")
SITE_VERSION = "0.1.0"

DATA_DIR = Path(os.environ.get("RMM_DATA_DIR", "/home/barn/data")).resolve()
DB_PATH = Path(os.environ.get("RMM_DB_PATH", str(DATA_DIR / "runchero-mirrors.db")))

MIRRORS_ROOT = Path(os.environ.get("RMM_MIRRORS_ROOT", "/home/barn/mirrors")).resolve()
ARCHIVE_DIR = Path(os.environ.get("RMM_ARCHIVE_DIR", str(MIRRORS_ROOT))).resolve()

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

DEFAULT_HOST = os.environ.get("RMM_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RMM_PORT", "8090"))

RUN_DIR = Path(os.environ.get("RMM_RUN_DIR", "/home/barn/run")).resolve()
LOG_DIR = Path(os.environ.get("RMM_LOG_DIR", "/home/barn/logs")).resolve()
PID_PATH = Path(os.environ.get("RMM_PID_PATH", str(RUN_DIR / "runchero-mirrors.pid")))
LOG_PATH = Path(os.environ.get("RMM_LOG_PATH", str(LOG_DIR / "runchero-mirrors.log")))

# HTTrack binary - prefer local bundled copy if present
HTTRACK_BIN = os.environ.get("RMM_HTTRACK_BIN") or ""
if not HTTRACK_BIN:
    # try local extracted copy
    local = Path("/tmp/httrack-root/usr/bin/httrack")
    if local.exists():
        HTTRACK_BIN = str(local)
    else:
        # try system
        import shutil
        HTTRACK_BIN = shutil.which("httrack") or "httrack"

HTTRACK_LIB = os.environ.get("RMM_HTTRACK_LIB") or ""
if not HTTRACK_LIB:
    local_lib = Path("/tmp/httrack-root/usr/lib/x86_64-linux-gnu")
    if local_lib.exists():
        HTTRACK_LIB = str(local_lib)

MAX_REQUEST_BYTES = 2 * 1024 * 1024
SECRET_KEY = os.environ.get("RMM_SECRET_KEY", "")


def ensure_dirs() -> None:
    for path in (DATA_DIR, MIRRORS_ROOT, RUN_DIR, LOG_DIR,
                 STATIC_DIR / "css", STATIC_DIR / "js",
                 STATIC_DIR / "img" / "icons", STATIC_DIR / "img" / "covers",
                 STATIC_DIR / "fonts"):
        path.mkdir(parents=True, exist_ok=True)
