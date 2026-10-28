"""Offer submission and deck endpoints.

Homepage shows a shuffled hand. Submitting an offer creates a new entry.
"""
from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Literal
import random
from datetime import datetime, timedelta

from app.db import get_session
from app import models, security
from app.config import settings

router = APIRouter(tags=["offers"])

# Seed deck data for initial load (copied from LinkDeck.html)
SEED_OFFERS = [
    {"b": "DoorDash", "c": "doordash.com", "o": "$25 off your first order", "k": "Food", "p": "pro", "u": 41, "d": 3, "l": "https://doordash.com/", "t": 2},
    {"b": "Uber Eats", "c": "ubereats.com", "o": "$20 off, orders over $25", "k": "Food", "p": "free", "u": 18, "d": 5, "l": "https://ubereats.com/", "t": 6},
    {"b": "Chime", "c": "chime.com", "o": "$100 when direct deposit hits", "k": "Banking", "p": "plus", "u": 33, "d": 7, "l": "https://chime.com/", "t": 10},
    {"b": "SoFi", "c": "sofi.com", "o": "Up to $300 sign-up bonus", "k": "Banking", "p": "free", "u": 12, "d": 6, "l": "https://sofi.com/", "t": 25},
    {"b": "Airbnb", "c": "airbnb.com", "o": "$40 off your first stay", "k": "Travel", "p": "boost", "u": 27, "d": 4, "l": "https://airbnb.com/", "t": 1},
    {"b": "Lyft", "c": "lyft.com", "o": "15% off your first 3 rides", "k": "Travel", "p": "free", "u": 9, "d": 3, "l": "https://lyft.com/", "t": 40},
    {"b": "Mint Mobile", "c": "mintmobile.com", "o": "First month on us", "k": "Phone", "p": "plus", "u": 22, "d": 5, "l": "https://mintmobile.com/", "t": 14},
    {"b": "Visible", "c": "visible.com", "o": "$20 off your first bill", "k": "Phone", "p": "free", "u": 7, "d": 3, "l": "https://visible.com/", "t": 60},
    {"b": "Coinbase", "c": "coinbase.com", "o": "$10 in crypto after first trade", "k": "Crypto", "p": "free", "u": 14, "d": 6, "l": "https://coinbase.com/", "t": 30},
    {"b": "Robinhood", "c": "robinhood.com", "o": "One free stock on signup", "k": "Crypto", "p": "plus", "u": 30, "d": 4, "l": "https://robinhood.com/", "t": 9},
    {"b": "Duolingo", "c": "duolingo.com", "o": "2 weeks of Super free", "k": "Apps", "p": "free", "u": 11, "d": 2, "l": "https://duolingo.com/", "t": 50},
    {"b": "Dropbox", "c": "dropbox.com", "o": "+500 MB storage for both of us", "k": "Apps", "p": "free", "u": 6, "d": 8, "l": "https://dropbox.com/", "t": 70},
    {"b": "Allbirds", "c": "allbirds.com", "o": "$25 off $100+", "k": "Shopping", "p": "pro", "u": 25, "d": 5, "l": "https://allbirds.com/", "t": 3},
]


class OfferSubmission(BaseModel):
    brand: str = Field(..., description="Brand name")
    link: str = Field(..., description="Affiliate/referral URL")
    headline: str = Field(..., max_length=140, description="Short offer description")
    category: str = Field(..., description="Category tag")
    plan: Literal["free", "plus", "pro", "boost"] = Field(..., description="User plan tier")


@router.get("/offers", response_model=List[dict])
async def list_offers(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    mode: Literal["shuffle", "top", "new", "one"] = Query("shuffle", description="Deck order mode"),
    db: AsyncSession = Depends(get_session),
):
    """Return offers in the deck according to mode & filters.

    In shuffle mode: each view gives a different random hand.
    Top/new: sorted by votes or created_at.
    One: single random pick (for demo).
    """
    from sqlalchemy import func

    ip_hash = security.sha256(request.client.host or "")
    query = select(models.Offer).where(models.Offer.status == models.OfferStatus.ACTIVE.value)
    if category and category != "All":
        query = query.where(models.Offer.category == category)

    all_offers = (await db.execute(query)).scalars().all()
    if mode == "top":
        all_offers.sort(key=lambda o: o.upvotes, reverse=True)
    elif mode == "new":
        all_offers.sort(key=lambda o: o.created_at, reverse=True)
    elif mode == "one":
        all_offers = random.choices(all_offers, k=1) if all_offers else []
    else:
        def shuffle_score(o):
            mult = settings.DEFAULT_MULTIPLIER.get(o.plan, 1)
            fresh = 1 + max(0, 1 - (datetime.utcnow() - o.created_at).total_seconds() / (14 * 86400))
            rate = (o.upvotes + 2) / (o.upvotes + o.downvotes + 4)
            seen = o.is_boosted or False
            return mult * fresh * (0.4 + rate) * (0.3 if seen else 1)
        if all_offers:
            total = sum(shuffle_score(o) for o in all_offers)
            all_offers.sort(key=lambda o: random.random() * shuffle_score(o) / total if total else 0.5)
            all_offers = all_offers[:6]
        else:
            all_offers = []

    return [o.public_card() for o in all_offers]


@router.post("/offers", response_model=dict, status_code=201)
async def submit_offer(
    submission: OfferSubmission = Body(...),
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
):
    """Submit a new offer. If authenticated, attaches to user; otherwise anonymous."""
    brand = submission.brand
    link = submission.link
    headline = submission.headline
    category = submission.category
    plan = submission.plan

    if not brand or not link or not headline:
        raise HTTPException(status_code=400, detail="Brand, link, and headline are required")

    domain = link.rstrip("/").split("/")[-1] or ""
    # Better domain extraction
    from urllib.parse import urlparse
    parsed = urlparse(link)
    domain = parsed.hostname or ""
    domain = domain.replace("www.", "") if domain else ""

    offer = models.Offer(
        brand=brand,
        domain=domain,
        headline=headline,
        promo=headline[:70],
        category=category,
        plan=plan,
        url=link,
        owner_id=user_id,
        anonymous_session=session_id,
        status=models.OfferStatus.PENDING.value,
    )
    db.add(offer)
    await db.flush()

    # If authenticated, create a PromoCode for tracking
    if user_id:
        code = __import__("secrets").token_urlsafe(8)
        db.add(models.PromoCode(
            offer_id=offer.id,
            user_id=user_id,
            code=code,
            kind="promo",
        ))
        await db.flush()

    await db.refresh(offer)
    return {"id": offer.id, "status": offer.status}


@router.get("/offers/seed")
async def seed_deck(db: AsyncSession = Depends(get_session)):
    """Populate initial seed offers (idempotent)."""
    from sqlalchemy import select, func

    count_stmt = select(func.count()).select_from(models.Offer)
    existing = (await db.execute(count_stmt)).scalar_one()
    if existing > 0:
        return {"message": f"Deck already has {existing} offers"}

    offers = []
    for s in SEED_OFFERS:
        domain = s["c"].replace("www.", "")
        offers.append(
            models.Offer(
                brand=s["b"],
                domain=domain,
                headline=s["o"],
                promo=s["o"],
                category=s["k"],
                plan=s["p"],
                url=s["l"],
                upvotes=s["u"],
                downvotes=s["d"],
                status=models.OfferStatus.ACTIVE.value,
                is_boosted=s["p"] == "boost",
                approved_at=datetime.utcnow(),
                owner_id=None,
            )
        )
    db.add_all(offers)
    await db.flush()

    return {"message": f"Seeded {len(offers)} offers"}