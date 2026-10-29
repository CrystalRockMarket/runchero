"""Click tracking: record a click on an offer and return stats."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, desc, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List, Optional

from app.db import get_session
from app import models, security

router = APIRouter(tags=["tracking"])


@router.post("/click/{offer_id}")
async def record_click(offer_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    """Record a click event for an offer. Client posts this from the outbound click handler."""
    ip_hash = security.sha256(security.client_ip(request))
    ua = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    stmt = select(models.Offer).where(models.Offer.id == offer_id)
    res = await db.execute(stmt)
    offer = res.scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    click = models.ClickEvent(
        offer_id=offer_id,
        user_id=None,
        ip_hash=ip_hash,
        user_agent=ua,
        referrer=referrer,
    )
    db.add(click)
    offer.clicks = (offer.clicks or 0) + 1

    await db.flush()
    return {"ok": True, "offer_id": offer_id, "clicked": True}


@router.post("/vote/{offer_id}")
async def vote(
    offer_id: int,
    request: Request,
    is_up: bool = True,
    voter_key: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
):
    """Record a worked / didn't-work vote. Deduplicated per offer+voter."""
    offer = (await db.execute(select(models.Offer).where(models.Offer.id == offer_id))).scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    key = (voter_key or "").strip()[:64]
    if not key:
        key = security.sha256(security.client_ip(request) + (request.headers.get("user-agent") or ""))

    existing = (
        await db.execute(
            select(models.Vote).where(
                models.Vote.offer_id == offer_id, models.Vote.voter_key == key
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        return {"ok": True, "already": True, "upvotes": offer.upvotes, "downvotes": offer.downvotes}

    db.add(models.Vote(offer_id=offer_id, voter_key=key, is_up=bool(is_up)))
    if is_up:
        offer.upvotes = (offer.upvotes or 0) + 1
    else:
        offer.downvotes = (offer.downvotes or 0) + 1
    await db.flush()
    return {"ok": True, "upvotes": offer.upvotes, "downvotes": offer.downvotes}


@router.get("/stats/offer/{offer_id}")
async def offer_stats(offer_id: int, db: AsyncSession = Depends(get_session)):
    """Aggregate stats for a single offer."""
    stmt = (
        select(
            func.count(models.ClickEvent.id),
            func.count(distinct(models.ClickEvent.ip_hash)),
        )
        .where(models.ClickEvent.offer_id == offer_id)
    )
    res = await db.execute(stmt)
    total, uniq = res.one()
    return {
        "offer_id": offer_id,
        "clicks": total or 0,
        "unique_visitors": uniq or 0,
    }


@router.get("/stats/global")
async def global_stats(db: AsyncSession = Depends(get_session)):
    """Global site-wide statistics (admin dashboard)."""
    from sqlalchemy import func

    offer_count = (await db.execute(select(func.count()).select_from(models.Offer))).scalar_one()
    click_count = (await db.execute(select(func.count()).select_from(models.ClickEvent))).scalar_one()
    user_count = (await db.execute(select(func.count()).select_from(models.User))).scalar_one()

    clicks_last_7d = (
        await db.execute(
            select(func.count(models.ClickEvent.id)).where(
                models.ClickEvent.created_at >= func.now() - __import__("datetime").timedelta(days=7)
            )
        )
    ).scalar_one()

    return {
        "offers": offer_count or 0,
        "clicks": click_count or 0,
        "unique_visitors": user_count or 0,
        "clicks_last_7d": clicks_last_7d or 0,
        "users": user_count or 0,
    }


@router.get("/stats/leaderboard")
async def leaderboard(db: AsyncSession = Depends(get_session)):
    """Referral leaderboard."""
    from sqlalchemy import func

    stmt = (
        select(models.Offer.brand, func.count(models.ClickEvent.id).label("clicks"))
        .join(models.ClickEvent, models.ClickEvent.offer_id == models.Offer.id)
        .where(models.Offer.status == models.OfferStatus.ACTIVE.value)
        .group_by(models.Offer.id, models.Offer.brand)
        .order_by(func.count(models.ClickEvent.id).desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    rows = []
    for row in result.all():
        rows.append({"brand": row[0], "clicks": row[1]})
    return rows
