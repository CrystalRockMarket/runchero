"""Runtime configuration for LinkDeck.

All settings are env-driven so the same code runs on a laptop, VPS, or CI.
"""
from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Core
    PROJECT_NAME: str = "LinkDeck"
    PROJECT_SHORT: str = "LD"
    PROJECT_TAGLINE: str = "Fair-shuffled affiliate & referral links"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Paths
    APP_DIR: Path = Path(__file__).resolve().parent
    PROJECT_DIR: Path = APP_DIR.parent
    DATA_DIR: Path = Path(os.environ.get("LD_DATA_DIR", "/home/barn/data")).resolve()
    DB_PATH: Path = Path(os.environ.get("LD_DB_PATH", str(DATA_DIR / "linkdeck.db")))
    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATES_DIR: Path = APP_DIR / "templates"

    # Network
    HOST: str = os.environ.get("LD_HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("LD_PORT", "8092"))

    # Security
    SECRET_KEY: str = os.environ.get("LD_SECRET_KEY", "dev-secret-change-me")
    ADMIN_PASSWORD: str = os.environ.get("LD_ADMIN_PASSWORD", "")
    ADMIN_SECRET: str = os.environ.get("LD_ADMIN_SECRET", "")
    ADMIN_SESSION_HOURS: int = int(os.environ.get("LD_ADMIN_SESSION_HOURS", "12"))
    SESSION_COOKIE_NAME: str = "ld_session"
    CSRF_COOKIE_NAME: str = "ld_csrf"
    RATE_LIMIT: str = "100/minute"
    RATE_LIMIT_ADMIN: str = "200/minute"

    # OAuth - Google
    GOOGLE_CLIENT_ID: str = os.environ.get("LD_GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.environ.get("LD_GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.environ.get(
        "LD_GOOGLE_REDIRECT_URI",
        f"http://localhost:{os.environ.get('LD_PORT', '8092')}/auth/google/callback",
    )

    # OAuth - Facebook
    FACEBOOK_APP_ID: str = os.environ.get("LD_FACEBOOK_APP_ID", "")
    FACEBOOK_APP_SECRET: str = os.environ.get("LD_FACEBOOK_APP_SECRET", "")
    FACEBOOK_REDIRECT_URI: str = os.environ.get(
        "LD_FACEBOOK_REDIRECT_URI",
        f"http://localhost:{os.environ.get('LD_PORT', '8092')}/auth/facebook/callback",
    )

    # Magic Link / Email
    SMTP_HOST: str = os.environ.get("LD_SMTP_HOST", "")
    SMTP_PORT: int = int(os.environ.get("LD_SMTP_PORT", "587"))
    SMTP_USER: str = os.environ.get("LD_SMTP_USER", "")
    SMTP_PASSWORD: str = os.environ.get("LD_SMTP_PASSWORD", "")
    SMTP_TLS: bool = os.environ.get("LD_SMTP_TLS", "1") not in ("0", "false", "no")
    MAIL_FROM: str = os.environ.get("LD_MAIL_FROM", "noreply@linkdeck.local")
    MAIL_FROM_NAME: str = os.environ.get("LD_MAIL_FROM_NAME", "LinkDeck")
    MAGIC_LINK_TTL_MINUTES: int = int(os.environ.get("LD_MAGIC_LINK_TTL_MINUTES", "15"))
    FRONTEND_BASE_URL: str = os.environ.get(
        "LD_FRONTEND_BASE_URL",
        f"http://localhost:{os.environ.get('LD_PORT', '8092')}",
    )

    # Feature flags
    ALLOW_ANONYMOUS_OFFER: bool = os.environ.get("LD_ALLOW_ANONYMOUS_OFFER", "1") not in ("0", "false", "no")
    ALLOW_REGISTRATION: bool = os.environ.get("LD_ALLOW_REGISTRATION", "1") not in ("0", "false", "no")
    REQUIRE_EMAIL_VERIFICATION: bool = os.environ.get("LD_REQUIRE_EMAIL_VERIFICATION", "0") not in ("0", "false", "no")

    # Business logic
    MAX_OFFERS_FREE: int = int(os.environ.get("LD_MAX_OFFERS_FREE", "1"))
    MAX_OFFERS_PLUS: int = int(os.environ.get("LD_MAX_OFFERS_PLUS", "5"))
    MAX_OFFERS_PRO: int = int(os.environ.get("LD_MAX_OFFERS_PRO", "20"))
    DEFAULT_MULTIPLIER: dict = {"free": 1, "plus": 3, "pro": 8, "boost": 10}
    BOOST_MULTIPLIER: int = 10
    BOOST_DURATION_HOURS: int = 24
    REFERRAL_POINTS_PER_SIGNUP: int = 1

    def ensure_dirs(self) -> None:
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.STATIC_DIR.mkdir(parents=True, exist_ok=True)
        (self.STATIC_DIR / "img").mkdir(parents=True, exist_ok=True)
        (self.STATIC_DIR / "css").mkdir(parents=True, exist_ok=True)
        (self.STATIC_DIR / "js").mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
settings.ensure_dirs()