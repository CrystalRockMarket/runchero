"""Authentication: Google, Facebook, email magic link, sessions."""
from __future__ import annotations

import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, security
from app.config import settings


def _smtp_configured() -> bool:
    return bool(settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD)


def send_magic_link_email(email: str, token: str, display_name: str) -> bool:
    """Send magic sign-in link. Returns True when dispatched."""
    if not _smtp_configured():
        return False
    msg = EmailMessage()
    msg["Subject"] = "Your LinkDeck sign-in link"
    msg["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
    msg["To"] = email
    body = (
        f"Hi {display_name},\n\n"
        f"Sign in to LinkDeck with this magic link (valid {settings.MAGIC_LINK_TTL_MINUTES} minutes):\n"
        f"{settings.FRONTEND_BASE_URL}/auth/magic/verify?token={token}\n\n"
        f"If you didn't ask for this, ignore this email.\n"
    )
    msg.set_content(body)
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            if settings.SMTP_TLS:
                smtp.starttls()
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception:
        return False


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.email == email.lower())
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def create_or_get_user(
    db: AsyncSession,
    email: str,
    display_name: str,
    provider: str,
    external_id: str = "",
) -> models.User:
    email = email.strip().lower()
    user = await get_user_by_email(db, email)
    if user is None:
        user = models.User(
            email=email,
            display_name=display_name or email.split("@")[0],
            auth_provider=provider,
            is_admin=False,
        )
        db.add(user)
        await db.flush()
    else:
        user.auth_provider = provider
        if display_name and user.display_name in ("", "User"):
            user.display_name = display_name
    return user


async def issue_magic_token(db: AsyncSession, user: models.User, ip: str) -> str:
    token = security.new_token()
    expires = datetime.utcnow() + timedelta(minutes=settings.MAGIC_LINK_TTL_MINUTES)
    db.add(
        models.MagicToken(
            user_id=user.id,
            token_hash=security.sha256(token),
            expires_at=expires,
            created_ip=ip,
        )
    )
    await db.flush()
    send_magic_link_email(user.email, token, user.display_name)
    return token


async def consume_magic_token(db: AsyncSession, token: str) -> Optional[models.User]:
    hashed = security.sha256(token)
    stmt = (
        select(models.MagicToken)
        .where(models.MagicToken.token_hash == hashed)
        .order_by(models.MagicToken.created_at.desc())
        .limit(1)
    )
    res = await db.execute(stmt)
    mt = res.scalar_one_or_none()
    if mt is None or mt.used_at is not None or mt.expires_at < datetime.utcnow():
        return None
    mt.used_at = datetime.utcnow()
    return mt.user


async def create_session(
    db: AsyncSession, user: models.User, ip: str, user_agent: str
) -> str:
    """Create a server-side session token and return the raw cookie value."""
    raw = security.new_token()
    expires = datetime.utcnow() + timedelta(days=30)
    db.add(
        models.SessionToken(
            user_id=user.id,
            token_hash=security.sha256(raw),
            expires_at=expires,
            created_ip=ip,
            user_agent=(user_agent or "")[:500],
        )
    )
    await db.flush()
    return raw


async def revoke_session(db: AsyncSession, raw: str) -> None:
    from sqlalchemy import delete

    await db.execute(
        delete(models.SessionToken).where(
            models.SessionToken.token_hash == security.sha256(raw)
        )
    )


async def bootstrap_admin(db: AsyncSession) -> Optional[models.User]:
    """Create the default admin from env if no admin exists."""
    stmt = select(models.User).where(models.User.is_admin.is_(True))
    res = await db.execute(stmt)
    admin = res.scalar_one_or_none()
    if admin is not None:
        return admin
    password = settings.ADMIN_PASSWORD
    if not password:
        return None
    admin = models.User(
        email="admin@linkdeck.local",
        display_name="LinkDeck Admin",
        auth_provider="password",
        is_admin=True,
        hashed_password=security.hash_password(password),
    )
    db.add(admin)
    await db.flush()
    return admin