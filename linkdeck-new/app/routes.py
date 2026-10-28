"""Page routes: home, submit, dashboard, login, logout, admin, magic."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth as auth_service, models
from app.db import get_session
from app.config import settings
from app.security import get_current_user_id

router = APIRouter()


def setup(templates: Jinja2Templates, get_user_id_fn):
    pass


def create_templates():
    return Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_session), user_id: int = 0):
    from sqlalchemy import select

    offers = []
    # Return a sample random hand for display
    stmt = (
        select(models.Offer)
        .where(models.Offer.status == models.OfferStatus.ACTIVE.value)
        .order_by(models.Offer.created_at.desc())
        .limit(6)
    )
    res = await db.execute(stmt)
    offers = res.scalars().all()

    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/submit", response_class=HTMLResponse)
async def submit(request: Request):
    return templates.TemplateResponse("submit.html", {"request": request})


@router.get("/plans", response_class=HTMLResponse)
async def plans(request: Request):
    return templates.TemplateResponse("plans.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_session), user_id: int = 0):
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    stmt = (
        select(models.User)
        .where(models.User.id == user_id)
        .options(models.selectinload(models.User.offers), models.selectinload(models.User.promo_codes), models.selectinload(models.User.referrals))
    )
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if user is None:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user},
    )


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return RedirectResponse(url="/", status_code=302)


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, db: AsyncSession = Depends(get_session), user_id: int = 0):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.get("/admin/panel", response_class=HTMLResponse)
async def admin_panel(request: Request, db: AsyncSession = Depends(get_session), user_id: int = 0):
    return templates.TemplateResponse("admin.html", {"request": request, "stats": {"offers": 0, "clicks": 0, "users": 0, "clicks_last_7d": 0}, "offers": [], "users": []})


@router.get("/magic/verify", response_class=HTMLResponse)
async def magic_verify(request: Request):
    return templates.TemplateResponse("magic_verify.html", {"request": request})
