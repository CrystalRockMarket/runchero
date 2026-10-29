"""Dependencies: current user resolution from session cookie."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, security
from app.db import get_session


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> Optional[models.User]:
    """Resolve the logged-in user from the session cookie, or None."""
    token = request.cookies.get(security.SESSION_COOKIE)
    if not token:
        return None
    hashed = security.sha256(token)
    stmt = (
        select(models.SessionToken)
        .where(models.SessionToken.token_hash == hashed)
        .order_by(models.SessionToken.created_at.desc())
        .limit(1)
    )
    res = await db.execute(stmt)
    st = res.scalar_one_or_none()
    if st is None or st.expires_at < datetime.utcnow():
        return None
    if not st.user or not st.user.is_active:
        return None
    return st.user


async def require_user(
    user: Optional[models.User] = Depends(get_current_user),
) -> models.User:
    from fastapi import HTTPException

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


async def require_admin(
    user: Optional[models.User] = Depends(get_current_user),
) -> models.User:
    from fastapi import HTTPException

    if user is None or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user