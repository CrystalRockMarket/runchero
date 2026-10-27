"""Configuration for the Runchero community hub."""
from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

SITE_NAME = os.environ.get("RHUB_SITE_NAME", "Runchero Hub")
SITE_SHORT = os.environ.get("RHUB_SITE_SHORT", "Hub")
SITE_TAGLINE = os.environ.get(
    "RHUB_SITE_TAGLINE", "Every community tool in one place."
)
SITE_BADGE = os.environ.get("RHUB_BADGE", "COMMUNITY DIRECTORY")
SITE_VERSION = "0.1.0"

DATA_DIR = Path(os.environ.get("RHUB_DATA_DIR", "/home/barn/data")).resolve()
DB_PATH = Path(os.environ.get("RHUB_DB_PATH", str(DATA_DIR / "runchero-hub.db")))

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

DEFAULT_HOST = os.environ.get("RHUB_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RHUB_PORT", "8092"))

RUN_DIR = Path(os.environ.get("RHUB_RUN_DIR", "/home/barn/run")).resolve()
LOG_DIR = Path(os.environ.get("RHUB_LOG_DIR", "/home/barn/logs")).resolve()
PID_PATH = Path(os.environ.get("RHUB_PID_PATH", str(RUN_DIR / "runchero-hub.pid")))
LOG_PATH = Path(os.environ.get("RHUB_LOG_PATH", str(LOG_DIR / "runchero-hub.log")))

SECRET_KEY = os.environ.get("RHUB_SECRET_KEY", "")
ADMIN_USER = os.environ.get("RHUB_ADMIN_USER", "runchero")
ADMIN_PASSWORD = os.environ.get("RHUB_ADMIN_PASSWORD", "runchero")
SECURE_COOKIES = os.environ.get("RHUB_SECURE_COOKIES", "0") in ("1", "true", "yes")
SESSION_MAX_AGE = 60 * 60 * 8

MAX_REQUEST_BYTES = 64 * 1024
MAX_NAME = 80
MAX_CONTACT = 120
MAX_TITLE = 120
MAX_DESCRIPTION = 2000
MAX_CATEGORY = 40
MAX_ADMIN_NOTE = 1000

SUBMISSIONS_PER_HOUR = int(os.environ.get("RHUB_SUBMISSIONS_PER_HOUR", "5"))
LOGIN_ATTEMPTS_PER_15_MIN = 12

STATUSES = ["new", "reviewing", "planned", "built", "declined"]
STATUS_LABELS = {
    "new": "New",
    "reviewing": "Reviewing",
    "planned": "Planned",
    "built": "Built",
    "declined": "Declined",
}

CATEGORIES = [
    "Farm",
    "Shop",
    "Library",
    "Mapping",
    "Websites",
    "Money",
    "Community",
    "Other",
]

EXCLUDED_TOKENS = (
    "earth.love",
    "earth_love",
    "earthlove",
    "games-earth",
    "games.earth",
    "games_earth",
    "gamesearth",
)

ADMIN_COOKIE = "rhub_admin"
CSRF_COOKIE = "rhub_csrf"

LINK_HOST = os.environ.get("RHUB_LINK_HOST", "").strip()
