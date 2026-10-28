"""Authentication: Google, Facebook, email magic link, password sessions."""
from __future__ import annotations

import os
import secrets
import smtplib
from email.message import EmailMessage
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from jinja2 import Environment

from app import models, security
from app.config import settings


def _smtp_configured() -> bool:
    return bool(settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD)


def send_magic_link_email(email: str, token: str, display_name: str) -> bool:
    """Send magic sign-in link. Returns True when dispatched."""
    if not _smtp_configured():
        return False
    if not settings.SMTP_HOST:
        return False
    msg = EmailMessage()
    msg["Subject"] = f"Your LinkDeck sign-in"
    msg["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
    msg["To"] = email
    body = (
        f"Hi {display_name},\n\n"
        f"Sign in to LinkDeck with this magic link (valid {settings.MAGIC_LINK_TTL_MINUTES} minutes):\n"
        f"https://{settings.FRONTEND_BASE_URL}/auth/magic/verify?token={token}\n\n"
        f"If you didn't ask for this, ignore this email.\n"
    )
    msg.set_content(body)
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        if settings.SMTP_TLS:
            smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(msg)
    return True


async def create_or_get_user(
    db: AsyncSession,
    email: str,
    display_name: str,
    provider: str,
    external_id: str,
) -> models.User:
    from sqlalchemy import update

    stmt = select(models.User).where(models.User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        user = models.User(
            email=email,
            display_name=display_name,
            auth_provider=provider,
            is_admin=False,
        )
        db.add(user)
        await db.flush()
    else:
        user.display_name = display_name
        user.auth_provider = provider
        user.picture_url = None
    return user


async def issue_magic_token(db: AsyncSession, user_id: int, email: str, display_name: str, ip: str) -> str:
    token = security.new_token()
    expires = __import__("datetime").datetime.utcnow() + __import__("datetime").timedelta(
        minutes=settings.MAGIC_LINK_TTL_MINUTES
    )
    db.add(
        models.MagicToken(
            user_id=user_id,
            token_hash=security.sha256(token),
            expires_at=expires,
            created_ip=ip,
        )
    )
    await db.flush()
    if _smtp_configured():
        send_magic_link_email(email, token, display_name)
    return token


async def consume_magic_token(db: AsyncSession, token: str) -> Optional[models.User]:
    from sqlalchemy import select

    hashed = security.sha256(token)
    stmt = (
        select(models.MagicToken)
        .where(models.MagicToken.token_hash == hashed)
        .order_by(models.MagicToken.created_at.desc())
        .limit(1)
    )
    res = await db.execute(stmt)
    mt = res.scalar_one_or_none()
    if mt is None or mt.used_at or mt.expires_at < __import__("datetime").datetime.utcnow():
        return None
    mt.used_at = __import__("datetime").datetime.utcnow()
    return mt.user


async def get_or_create_admin(db: AsyncSession, password: str) -> models.User | None:
    from sqlalchemy import select

    stmt = select(models.User).where(models.User.is_admin.is_(True))
    res = await db.execute(stmt)
    admin = res.scalar_one_or_none()
    if admin is None:
        admin = models.User(
            email=f"admin@{settings.PROJECT_NAME.lower()}.local",
            display_name="LinkDeck Admin",
            auth_provider="password",
            is_admin=True,
        )
        admin.hashed_password = security.hash_password(password)
        db.add(admin)
        await db.flush()
    return admin
