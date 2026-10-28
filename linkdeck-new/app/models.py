"""Database models for LinkDeck.

All tracking data is persisted here. Offers are the central object:
each Offer belongs to a User (or is anonymous), accumulates ClickEvents,
Votes, and optional PromoCode rows.
"""
from __future__ import annotations

import enum
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.config import settings

CATS = ["Food", "Banking", "Travel", "Phone", "Crypto", "Apps", "Shopping"]
PLAN_CHOICES = ["free", "plus", "pro", "boost"]


class Base(DeclarativeBase):
    pass


class OfferStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REJECTED = "rejected"
    FLAGGED = "flagged"


class AuthProvider(str, enum.Enum):
    EMAIL_LINK = "email_link"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    PASSWORD = "password"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False, default="User")
    picture_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    auth_provider: Mapped[str] = mapped_column(String(20), default=AuthProvider.PASSWORD.value)
    hashed_password: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    offers: Mapped[list["Offer"]] = relationship(back_populates="owner", lazy="selectin")
    promo_codes: Mapped[list["PromoCode"]] = relationship(back_populates="user", lazy="selectin")
    magic_tokens: Mapped[list["MagicToken"]] = relationship(back_populates="user", lazy="selectin")
    referrals: Mapped[list["Referral"]] = relationship(
        foreign_keys="Referral.referrer_id", back_populates="referrer", lazy="selectin"
    )

    def public_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "picture_url": self.picture_url,
            "auth_provider": self.auth_provider,
            "is_admin": self.is_admin,
        }


class Offer(Base):
    __tablename__ = "offers"
    __table_args__ = (
        Index("ix_offers_owner_status", "owner_id", "status"),
        Index("ix_offers_status_created", "status", "created_at"),
        Index("ix_offers_domain", "domain"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(80), index=True)
    domain: Mapped[str] = mapped_column(String(63))
    headline: Mapped[str] = mapped_column(String(140))
    promo: Mapped[str] = mapped_column(String(140))
    category: Mapped[str] = mapped_column(String(40), default="Apps")
    plan: Mapped[str] = mapped_column(String(10), default="free")
    url: Mapped[str] = mapped_column(String(500))
    owner_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    anonymous_session: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default=OfferStatus.PENDING.value)
    is_boosted: Mapped[bool] = mapped_column(Boolean, default=False)
    boost_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    downvotes: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    owner: Mapped[Optional[User]] = relationship(
        "User", back_populates="offers", lazy="joined", foreign_keys=[owner_id]
    )
    click_events: Mapped[list["ClickEvent"]] = relationship(back_populates="offer", cascade="all, delete-orphan")
    votes: Mapped[list["Vote"]] = relationship(back_populates="offer", cascade="all, delete-orphan")
    promo_codes: Mapped[list["PromoCode"]] = relationship(back_populates="offer", cascade="all, delete-orphan")

    @property
    def is_live(self) -> bool:
        return self.status == OfferStatus.ACTIVE.value

    @property
    def age_hours(self) -> int:
        return int((datetime.utcnow() - self.created_at).total_seconds() // 3600)

    def public_card(self, viewer_id: Optional[int] = None, boosted: bool = False) -> dict:
        return {
            "id": self.id,
            "brand": self.brand,
            "domain": self.domain,
            "offer": self.headline,
            "promo": self.promo,
            "category": self.category,
            "plan": self.plan,
            "url": self.url,
            "is_boosted": self.is_boosted or boosted,
            "is_live": self.is_live,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "clicks": self.clicks,
            "age_hours": self.age_hours,
            "can_vote": viewer_id is None or viewer_id != self.owner_id,
        }


class ClickEvent(Base):
    __tablename__ = "click_events"
    __table_args__ = (
        Index("ix_clicks_offer_at", "offer_id", "created_at"),
        Index("ix_clicks_user_at", "user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    ip_hash: Mapped[str] = mapped_column(String(64))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    referrer: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), index=True)

    offer: Mapped["Offer"] = relationship("Offer", back_populates="click_events", lazy="joined")


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint("offer_id", "user_id", name="uq_votes_offer_user"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    is_up: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    offer: Mapped["Offer"] = relationship("Offer", back_populates="votes")


class PromoCode(Base):
    __tablename__ = "promo_codes"
    __table_args__ = (
        Index("ix_promos_offer", "offer_id"),
        Index("ix_promos_user", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    code: Mapped[str] = mapped_column(String(60), index=True)
    kind: Mapped[str] = mapped_column(String(20), default="promo")
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    redemptions: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    offer: Mapped["Offer"] = relationship("Offer", back_populates="promo_codes", lazy="joined")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="promo_codes")


class MagicToken(Base):
    __tablename__ = "magic_tokens"
    __table_args__ = (
        Index("ix_tokens_token", "token_hash"),
        Index("ix_tokens_user", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="magic_tokens")


class Referral(Base):
    __tablename__ = "referrals"
    __table_args__ = (
        UniqueConstraint("referral_code", "referred_email", name="uq_ref_code_email"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    referred_user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    referred_email: Mapped[str] = mapped_column(String(254), index=True)
    referral_code: Mapped[str] = mapped_column(String(12), index=True)
    converted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    referrer: Mapped["User"] = relationship(
        "User", foreign_keys=[referrer_id], back_populates="referrals"
    )


class SessionToken(Base):
    __tablename__ = "session_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    created_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship("User", lazy="joined")


def _mult(plan: str) -> int:
    return settings.DEFAULT_MULTIPLIER.get(plan, 1)