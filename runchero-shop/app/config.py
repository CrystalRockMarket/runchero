"""Runtime configuration for the Runchero Beef shop.

This is a separate process from the Runchero Information Depo. It listens on
its own port, keeps its own database, and never touches the depot's files.
Every path can be overridden with an environment variable so the same code
runs on the farm box, a laptop, or a shared server.
"""
from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

#: Human readable product name (shown in title bar, logo, footer).
SITE_NAME = os.environ.get("RBS_SITE_NAME", "Runchero Beef")
SITE_SHORT = os.environ.get("RBS_SITE_SHORT", "Runchero")
SITE_TAGLINE = os.environ.get(
    "RBS_SITE_TAGLINE", "Locally grown beef, cut for your table."
)
SITE_BADGE = os.environ.get("RBS_BADGE", "DEMO")
SITE_VERSION = "0.1.0"

#: Where the shop lives and who is behind it.
LOCALE = os.environ.get("RBS_LOCALE", "Shelbyville, Kentucky")
FACEBOOK_URL = os.environ.get("RBS_FACEBOOK_URL", "")
CONTACT_EMAIL = os.environ.get("RBS_CONTACT_EMAIL", "hello@runchero.example")

#: Public base URL. Used for canonical links, Open Graph tags, the sitemap
#: and robots.txt. Left empty, the shop falls back to the host it was asked
#: for, so it still works behind a proxy on a different name.
SITE_URL = os.environ.get("RBS_SITE_URL", "").rstrip("/")

#: Data roots. The database is the whole store.
DATA_DIR = Path(os.environ.get("RBS_DATA_DIR", "/home/barn/data")).resolve()
DB_PATH = Path(os.environ.get("RBS_DB_PATH", str(DATA_DIR / "runchero-shop.db")))

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

#: Network
DEFAULT_HOST = os.environ.get("RBS_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RBS_PORT", "8081"))

#: Service files, kept out of the project so a redeploy never eats them.
RUN_DIR = Path(os.environ.get("RBS_RUN_DIR", "/home/barn/run")).resolve()
LOG_DIR = Path(os.environ.get("RBS_LOG_DIR", "/home/barn/logs")).resolve()
PID_PATH = Path(os.environ.get("RBS_PID_PATH", str(RUN_DIR / "runchero-shop.pid")))
LOG_PATH = Path(os.environ.get("RBS_LOG_PATH", str(LOG_DIR / "runchero-shop.log")))

#: Payments. "mock" keeps the shop fully offline; "stripe" calls Stripe's REST
#: API over urllib so no SDK is needed.
PAYMENT_PROVIDER = os.environ.get("RBS_PAYMENT_PROVIDER", "mock").lower()
STRIPE_SECRET_KEY = os.environ.get("RBS_STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("RBS_STRIPE_PUBLISHABLE_KEY", "")
CURRENCY = os.environ.get("RBS_CURRENCY", "usd")

#: Sessions and admin. A generated secret is used if none is supplied, which
#: means sessions drop on restart, which is fine for a demo.
SECRET_KEY = os.environ.get("RBS_SECRET_KEY", "")
ADMIN_USER = os.environ.get("RBS_ADMIN_USER", "runchero")
ADMIN_PASSWORD = os.environ.get("RBS_ADMIN_PASSWORD", "")

#: Outbound HTTP for the market price job.
HTTP_TIMEOUT = int(os.environ.get("RBS_HTTP_TIMEOUT", "30"))
USER_AGENT = os.environ.get(
    "RBS_USER_AGENT", f"{SITE_NAME}/1.0 (+https://{SITE_SHORT.lower()}.example)"
)

#: Optional USDA AMS API key. The shop works without it: the keyless feeds
#: cover national weekly and monthly prices, and the key only adds regional
#: detail.
AMS_API_KEY = os.environ.get("RBS_AMS_API_KEY", "")

#: Hard cap on a request body, 2 MB. Enough for a big cart, small enough that
#: a runaway form cannot exhaust the box.
MAX_REQUEST_BYTES = 2 * 1024 * 1024


def ensure_dirs() -> None:
    for path in (DATA_DIR, RUN_DIR, LOG_DIR, STATIC_DIR / "img" / "icons",
                 STATIC_DIR / "img" / "tiles", STATIC_DIR / "img" / "uploads",
                 STATIC_DIR / "css", STATIC_DIR / "fonts"):
        path.mkdir(parents=True, exist_ok=True)
