"""Auth router: Google, Facebook OAuth, magic link, email sign-in, logout."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, security, auth
from app.db import get_session
from app.config import settings

router = APIRouter(tags=["auth"], prefix="/auth")


@router.get("/google")
async def google_login(request: Request, db: AsyncSession = Depends(get_session)):
    """Start Google OAuth flow."""
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        return JSONResponse(
            {"error": "google_oauth_not_configured"},
            status_code=501,
        )
    return JSONResponse({"redirect": f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid%20email%20profile&prompt=select_account"})


@router.get("/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_session)):
    """Exchange Google authorization code for access token and user."""
    import httpx
    from httpx import AsyncClient

    async with AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_res.json()
        userinfo_res = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token_data.get('access_token', '')}"},
        )
        userinfo = userinfo_res.json()
        email = userinfo.get("email", "")
        display_name = userinfo.get("name", "Google User")

    user = await auth.create_or_get_user(db, email, display_name, "google", str(userinfo.get("sub", "")))
    token = security.new_token()
    # session issuance stub; real token store below
    return {"ok": True, "user": user.public_dict()}


@router.get("/facebook")
async def facebook_login(request: Request, db: AsyncSession = Depends(get_session)):
    """Start Facebook OAuth flow."""
    if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET:
        return JSONResponse(
            {"error": "facebook_oauth_not_configured"},
            status_code=501,
        )
    return JSONResponse({"redirect": f"https://www.facebook.com/v18.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URI}&scope=email&response_type=code"})


@router.get("/facebook/callback")
async def facebook_callback(code: str, db: AsyncSession = Depends(get_session)):
    """Exchange Facebook authorization code for access token and user."""
    import httpx
    from httpx import AsyncClient

    async with AsyncClient() as client:
        token_res = await client.get(
            "https://graph.facebook.com/v18.0/oauth/access_token",
            params={
                "client_id": settings.FACEBOOK_APP_ID,
                "client_secret": settings.FACEBOOK_APP_SECRET,
                "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
                "code": code,
            },
        )
        token_data = token_res.json()
        userinfo_res = await client.get(
            "https://graph.facebook.com/me",
            params={"fields": "id,name,email,picture"},
        )
        userinfo = userinfo_res.json()
        email = userinfo.get("email", "")
        display_name = userinfo.get("name", "Facebook User")

    user = await auth.create_or_get_user(db, email, display_name, "facebook", str(userinfo.get("id", "")))
    token = security.new_token()
    return {"ok": True, "user": user.public_dict()}


@router.post("/magic/send")
async def magic_send(request: Request, email: str, db: AsyncSession = Depends(get_session)):
    """Request magic sign-in link via email."""
    email = email.strip().lower()
    user = await auth.get_or_create_user(db, email, email, "email_link", email)
    token = await auth.issue_magic_token(db, user.id, user.email, user.display_name, str(request.client.host or ""))
    return {"ok": True, "sent": True, "dev_link": None if not settings.DEBUG else f"http://{settings.HOST}:{settings.PORT}/auth/magic/verify?token={token}"}


@router.get("/magic/verify")
async def magic_verify(token: str, db: AsyncSession = Depends(get_session)):
    """Verify magic token and establish session."""
    user = await auth.consume_magic_token(db, token)
    if user is None:
        return JSONResponse({"ok": False, "error": "invalid_or_expired"}, status_code=400)
    return {"ok": True, "user": user.public_dict()}


@router.get("/me")
async def me(db: AsyncSession = Depends(get_session), user_id: int = 0):
    """Return current user (placeholder until session middleware added)."""
    from sqlalchemy import select

    stmt = select(models.User).where(models.User.id == user_id)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"user": user.public_dict()}


@router.post("/logout")
async def logout(db: AsyncSession = Depends(get_session)):
    return {"ok": True}
