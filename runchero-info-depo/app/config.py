"""Runtime configuration for the Runchero Information Depo.

Every path can be overridden with an environment variable so the same code
runs on a workshop laptop, a Raspberry Pi in the barn, or a shared server.
"""
from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

#: Human readable product name (shown in title bar, logo, footer).
SITE_NAME = os.environ.get("RID_SITE_NAME", "Runchero Information Depo")
SITE_SHORT = os.environ.get("RID_SITE_SHORT", "RID")
SITE_TAGLINE = "A sourced field library, available offline."
SITE_BADGE = os.environ.get("RID_BADGE", "DEMO")
SITE_VERSION = "0.1.0"

#: Data roots. The database lives on the box, ebooks live in the archive.
DATA_DIR = Path(os.environ.get("RID_DATA_DIR", "/home/barn/data")).resolve()
ARCHIVE_DIR = Path(os.environ.get("RID_ARCHIVE_DIR", "/home/barn/archive")).resolve()
DB_PATH = Path(os.environ.get("RID_DB_PATH", str(DATA_DIR / "runchero.db")))

#: Where uploaded ebooks would land (submission flow, admin phase).
UPLOAD_DIR = ARCHIVE_DIR / "inbox"

TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

#: Network
DEFAULT_HOST = os.environ.get("RID_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("RID_PORT", "8080"))

#: Hard cap for a single upload / download stream, 512 MB.
MAX_UPLOAD_BYTES = 512 * 1024 * 1024

#: Compatibility flag for read-only demos. Submissions/admin stay available.
READ_ONLY = os.environ.get("RID_READ_ONLY", "0") not in ("0", "false", "no")

#: Admin review panel. Set either RID_ADMIN_PASSWORD or store a hash with
#: tools/admin_password.py. Sessions are signed with a local secret file.
ADMIN_PASSWORD = os.environ.get("RID_ADMIN_PASSWORD", "")
ADMIN_SECRET = os.environ.get("RID_ADMIN_SECRET", "")
ADMIN_SESSION_SECONDS = int(os.environ.get("RID_ADMIN_SESSION_HOURS", "12")) * 3600

#: Public request limits.
MAX_FORM_BYTES = 256 * 1024


def ensure_dirs() -> None:
    for path in (DATA_DIR, ARCHIVE_DIR, UPLOAD_DIR, STATIC_DIR / "img" / "covers",
                 STATIC_DIR / "img" / "icons", STATIC_DIR / "img" / "tiles"):
        path.mkdir(parents=True, exist_ok=True)
