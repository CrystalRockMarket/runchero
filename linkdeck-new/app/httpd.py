"""FastAPI application factory: middleware, security headers, routers, static."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app import models
from app.api import admin as admin_api
from app.api import auth_router, offers, tracking
from app.config import settings
from app.db import get_session, init_db, async_session_maker
from app.deps import get_current_user
from app.security import limiter


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds production-grade security headers to every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        csp = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "script-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers["Content-Security-Policy"] = csp
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await _bootstrap()
    yield


async def _bootstrap() -> None:
    """Seed the deck and create the default admin if configured."""
    from app import auth as auth_service
    from app.api.offers import SEED_OFFERS, make_code

    async with async_session_maker() as db:
        try:
            count = (await db.execute(select(func.count()).select_from(models.Offer))).scalar_one()
            if count == 0:
                now = __import__("datetime").datetime.utcnow()
                db.add_all([
                    models.Offer(
                        brand=s["b"],
                        domain=s["c"].replace("www.", ""),
                        headline=s["o"],
                        promo=s["o"],
                        code=s.get("x") or make_code(s["b"]),
                        category=s["k"],
                        plan=s["p"],
                        url=s["l"],
                        upvotes=s["u"],
                        downvotes=s["d"],
                        status=models.OfferStatus.ACTIVE.value,
                        is_boosted=s["p"] == "boost",
                        approved_at=now,
                        created_at=now - __import__("datetime").timedelta(hours=s["t"]),
                    )
                    for s in SEED_OFFERS
                ])
            # Backfill promo codes for offers created before the code column existed.
            missing = (
                await db.execute(select(models.Offer).where(models.Offer.code.is_(None)))
            ).scalars().all()
            for offer in missing:
                offer.code = make_code(offer.brand)
            await auth_service.bootstrap_admin(db)
            await db.commit()
        except Exception:
            await db.rollback()
            raise


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Fair-shuffled affiliate & referral links with click tracking",
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

app.include_router(auth_router.router, prefix="/auth")
app.include_router(offers.router, prefix="/api")
app.include_router(tracking.router, prefix="/api")
app.include_router(admin_api.router, prefix="/api")


def _ctx(request: Request, user: Optional[models.User] = None, **extra) -> dict:
    ctx = {"request": request, "user": user, "settings": settings}
    ctx.update(extra)
    return ctx


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
):
    return templates.TemplateResponse(request, "index.html", _ctx(request, user))


@app.get("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
):
    return templates.TemplateResponse(request, "submit.html", _ctx(request, user))


@app.get("/plans", response_class=HTMLResponse)
async def plans(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
):
    return templates.TemplateResponse(request, "plans.html", _ctx(request, user))


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    stmt = (
        select(models.User)
        .where(models.User.id == user.id)
        .options(
            selectinload(models.User.offers),
            selectinload(models.User.promo_codes),
            selectinload(models.User.referrals),
        )
    )
    fresh = (await db.execute(stmt)).scalar_one_or_none()
    if fresh is None:
        return RedirectResponse(url="/login", status_code=302)
    # Aggregate click stats for this user's offers
    offer_ids = [o.id for o in fresh.offers]
    total_clicks = 0
    unique_visitors = 0
    recent = []
    if offer_ids:
        total_clicks = (
            await db.execute(
                select(func.count(models.ClickEvent.id)).where(
                    models.ClickEvent.offer_id.in_(offer_ids)
                )
            )
        ).scalar_one()
        unique_visitors = (
            await db.execute(
                select(func.count(func.distinct(models.ClickEvent.ip_hash))).where(
                    models.ClickEvent.offer_id.in_(offer_ids)
                )
            )
        ).scalar_one()
        recent = (
            await db.execute(
                select(models.ClickEvent)
                .where(models.ClickEvent.offer_id.in_(offer_ids))
                .order_by(models.ClickEvent.created_at.desc())
                .limit(20)
            )
        ).scalars().all()
    stats = {
        "offers": len(fresh.offers),
        "clicks": total_clicks or 0,
        "unique_visitors": unique_visitors or 0,
        "recent": recent,
    }
    return templates.TemplateResponse(
        request, "dashboard.html", _ctx(request, user, stats=stats)
    )


@app.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
):
    if user is not None:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse(request, "login.html", _ctx(request, user))


@app.get("/logout")
async def logout(request: Request):
    from app import security

    token = request.cookies.get(security.SESSION_COOKIE)
    if token:
        async with async_session_maker() as db:
            from app import auth as auth_service

            await auth_service.revoke_session(db, token)
            await db.commit()
    resp = RedirectResponse(url="/", status_code=302)
    resp.delete_cookie(security.SESSION_COOKIE, path="/")
    return resp


@app.get("/admin", response_class=HTMLResponse)
async def admin(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
):
    if user is not None and user.is_admin:
        return RedirectResponse(url="/admin/panel", status_code=302)
    return templates.TemplateResponse(request, "admin_login.html", _ctx(request, user))


@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return RedirectResponse(url="/admin", status_code=302)


@app.get("/admin/panel", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    user: Optional[models.User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if user is None or not user.is_admin:
        return RedirectResponse(url="/admin", status_code=302)

    offer_count = (await db.execute(select(func.count()).select_from(models.Offer))).scalar_one()
    click_count = (await db.execute(select(func.count()).select_from(models.ClickEvent))).scalar_one()
    user_count = (await db.execute(select(func.count()).select_from(models.User))).scalar_one()
    pending_count = (
        await db.execute(
            select(func.count()).select_from(models.Offer).where(
                models.Offer.status == models.OfferStatus.PENDING.value
            )
        )
    ).scalar_one()

    offers = (
        await db.execute(select(models.Offer).order_by(models.Offer.created_at.desc()).limit(200))
    ).scalars().all()
    users = (
        await db.execute(select(models.User).order_by(models.User.created_at.desc()).limit(200))
    ).scalars().all()

    stats = {
        "offers": offer_count or 0,
        "clicks": click_count or 0,
        "users": user_count or 0,
        "pending": pending_count or 0,
    }
    return templates.TemplateResponse(
        request,
        "admin.html",
        _ctx(request, user, stats=stats, offers=offers, users=users),
    )


@app.get("/magic/verify", response_class=HTMLResponse)
async def magic_verify_page(request: Request):
    # Handled by /auth/magic/verify; this is a friendly fallback.
    return RedirectResponse(url="/login", status_code=302)


@app.get("/health")
async def health():
    return {"ok": True, "version": settings.VERSION, "name": settings.PROJECT_NAME}


@app.get("/robots.txt")
async def robots():
    return HTMLResponse(
        "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /dashboard\n",
        media_type="text/plain",
    )