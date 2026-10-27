"""Configuration for Runchero Links.

Every setting can be overridden with an environment variable so the same code
runs on the farm box or a laptop without edits.
"""
from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

SITE_NAME = os.environ.get("RLK_SITE_NAME", "Runchero Links")
SITE_SHORT = os.environ.get("RLK_SITE_SHORT", "Links")
SITE_TAGLINE = os.environ.get(
    "RLK_SITE_TAGLINE", "Turn everyday Amazon links into community support."
)
SITE_BADGE = os.environ.get("RLK_BADGE", "COMMUNITY TOOL")
SITE_VERSION = "0.1.0"

AFFILIATE_TAG = os.environ.get("RLK_AFFILIATE_TAG", "runchero-20").strip()
AMAZON_SITE = "https://www.amazon.com"

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

DEFAULT_HOST = os.environ.get("RLK_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RLK_PORT", "8091"))

RUN_DIR = Path(os.environ.get("RLK_RUN_DIR", "/home/barn/run")).resolve()
LOG_DIR = Path(os.environ.get("RLK_LOG_DIR", "/home/barn/logs")).resolve()
PID_PATH = Path(os.environ.get("RLK_PID_PATH", str(RUN_DIR / "runchero-links.pid")))
LOG_PATH = Path(os.environ.get("RLK_LOG_PATH", str(LOG_DIR / "runchero-links.log")))

MAX_REQUEST_BYTES = 64 * 1024
MAX_URL_LENGTH = 2000
MAX_BULK_LINKS = 50
MAX_KEYWORDS_LENGTH = 200

RESOLVE_TIMEOUT = float(os.environ.get("RLK_RESOLVE_TIMEOUT", "5"))
RESOLVE_MAX_REDIRECTS = 5
RESOLVE_MATCHES_PER_MINUTE = int(os.environ.get("RLK_RESOLVE_PER_MINUTE", "30"))

DEFAULT_COMMISSION_RATE = float(os.environ.get("RLK_COMMISSION_RATE", "3.0"))
MIN_COMMISSION_RATE = 1.0
MAX_COMMISSION_RATE = 10.0

EXAMPLE_SEARCHES = [
    "canning jars",
    "pressure canner",
    "fermentation crock",
    "cast-iron skillet",
    "garden drip kit",
    "chicken coop",
]

EXAMPLE_PRICES = [25, 50, 100, 250]

DISCLOSURE = (
    "As an Amazon Associate, Runchero earns from qualifying purchases. "
    "Links on this page are affiliate links."
)
