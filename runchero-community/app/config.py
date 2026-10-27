"""Configuration for the Runchero Community Directory."""
from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

SITE_NAME = os.environ.get("RDIR_SITE_NAME", "Runchero Community Directory")
SITE_SHORT = os.environ.get("RDIR_SITE_SHORT", "Community")
SITE_TAGLINE = os.environ.get(
    "RDIR_SITE_TAGLINE", "The people of Runchero, all in one place."
)
SITE_BADGE = os.environ.get("RDIR_BADGE", "NEIGHBOURS")
SITE_VERSION = "0.1.0"

DATA_DIR = Path(os.environ.get("RDIR_DATA_DIR", "/home/barn/data")).resolve()
DB_PATH = Path(os.environ.get(
    "RDIR_DB_PATH", str(DATA_DIR / "runchero-community.db")
))

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

DEFAULT_HOST = os.environ.get("RDIR_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RDIR_PORT", "8093"))

RUN_DIR = Path(os.environ.get("RDIR_RUN_DIR", "/home/barn/run")).resolve()
LOG_DIR = Path(os.environ.get("RDIR_LOG_DIR", "/home/barn/logs")).resolve()
PID_PATH = Path(os.environ.get(
    "RDIR_PID_PATH", str(RUN_DIR / "runchero-community.pid")
))
LOG_PATH = Path(os.environ.get(
    "RDIR_LOG_PATH", str(LOG_DIR / "runchero-community.log")
))

SECRET_KEY = os.environ.get("RDIR_SECRET_KEY", "")
ADMIN_USER = os.environ.get("RDIR_ADMIN_USER", "runchero")
ADMIN_PASSWORD = os.environ.get("RDIR_ADMIN_PASSWORD", "runchero")
SECURE_COOKIES = os.environ.get("RDIR_SECURE_COOKIES", "0") in ("1", "true", "yes")
SESSION_MAX_AGE = 60 * 60 * 8

MAX_REQUEST_BYTES = 64 * 1024
MAX_NAME = 120
MAX_DESCRIPTION = 2000
MAX_LOCATION = 120
MAX_SUBMITTER = 120
MAX_CHANNEL_LABEL = 40
MAX_CHANNEL_VALUE = 500
MAX_ADMIN_NOTE = 1000
MAX_CUSTOM = 3

SUBMISSIONS_PER_HOUR = int(os.environ.get("RDIR_SUBMISSIONS_PER_HOUR", "5"))
LOGIN_ATTEMPTS_PER_15_MIN = 12

CATEGORIES = [
    "Neighbours",
    "Skills & Help",
    "Garden & Farm",
    "Trades & Repairs",
    "Care & Support",
    "Health",
    "Education",
    "Faith",
    "Community",
    "Emergency",
    "Other",
]

ADMIN_COOKIE = "rdir_admin"
CSRF_COOKIE = "rdir_csrf"
