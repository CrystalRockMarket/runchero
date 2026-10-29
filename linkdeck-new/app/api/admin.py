"""Admin API: moderate offers, inspect users and stats. Requires admin login."""
from __future__ import annotations

import os
from typing import Literal, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.db import get_session
from app.deps import require_admin

router = APIRouter(tags=["admin"], prefix="/admin")


class StatusUpdate(BaseModel):
    status: Literal["active", "rejected", "pending", "flagged"]


@router.post("/offers/{offer_id}/status")
async def set_offer_status(
    offer_id: int,
    payload: StatusUpdate,
    admin: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_session),
):
    offer = (await db.execute(select(models.Offer).where(models.Offer.id == offer_id))).scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    offer.status = payload.status
    if payload.status == models.OfferStatus.ACTIVE.value:
        offer.approved_at = __import__("datetime").datetime.utcnow()
    await db.flush()
    return {"ok": True, "id": offer.id, "status": offer.status}


@router.delete("/offers/{offer_id}")
async def delete_offer(
    offer_id: int,
    admin: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_session),
):
    offer = (await db.execute(select(models.Offer).where(models.Offer.id == offer_id))).scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    await db.delete(offer)
    return {"ok": True, "deleted": offer_id}


@router.get("/stats")
async def admin_stats(
    admin: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_session),
):
    by_status = {}
    for status in ("pending", "active", "rejected", "flagged"):
        by_status[status] = (
            await db.execute(
                select(func.count()).select_from(models.Offer).where(models.Offer.status == status)
            )
        ).scalar_one()
    total_clicks = (await db.execute(select(func.count()).select_from(models.ClickEvent))).scalar_one()
    total_users = (await db.execute(select(func.count()).select_from(models.User))).scalar_one()
    return {
        "by_status": by_status,
        "total_clicks": total_clicks or 0,
        "total_users": total_users or 0,
    }


@router.get("/clicks")
async def admin_clicks(
    admin: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_session),
    limit: int = 100,
):
    limit = min(max(limit, 1), 500)
    rows = (
        await db.execute(
            select(models.ClickEvent)
            .order_by(models.ClickEvent.created_at.desc())
            .limit(limit)
        )
    ).scalars().all()
    return [
        {
            "id": c.id,
            "offer_id": c.offer_id,
            "user_id": c.user_id,
            "at": c.created_at.isoformat() if c.created_at else None,
            "referrer": c.referrer,
        }
        for c in rows
    ]