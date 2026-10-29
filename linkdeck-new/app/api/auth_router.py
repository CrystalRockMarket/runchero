"""Auth routes: Google, Facebook OAuth, magic link, admin login, logout.

Included with prefix /auth, so paths here are relative (e.g. "/google" -> /auth/google).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth as auth_service, models, security
from app.config import settings
from app.db import get_session
from app.security import limiter

router = APIRouter(tags=["auth"])


def _set_session_cookie(response, token: str) -> None:
    secure = settings.FRONTEND_BASE_URL.startswith("https")
    response.set_cookie(
        security.SESSION_COOKIE,
        token,
        max_age=30 * 24 * 3600,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )


async def _finish_login(request: Request, db: AsyncSession, user: models.User):
    raw = await auth_service.create_session(
        db, user, security.client_ip(request), request.headers.get("user-agent", "")
    )
    resp = RedirectResponse(url="/dashboard", status_code=302)
    _set_session_cookie(resp, raw)
    return resp


@router.get("/google")
async def google_login(request: Request):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        return RedirectResponse(url="/login?error=google_not_configured", status_code=302)
    from urllib.parse import urlencode

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "select_account",
    }
    return RedirectResponse(
        "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params), status_code=302
    )


@router.get("/google/callback")
async def google_callback(code: str, request: Request, db: AsyncSession = Depends(get_session)):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        return RedirectResponse(url="/login?error=google_not_configured", status_code=302)
    import httpx

    async with httpx.AsyncClient(timeout=15) as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_res.json()
        access = token_data.get("access_token")
        if not access:
            return RedirectResponse(url="/login?error=google_token", status_code=302)
        info_res = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access}"},
        )
        info = info_res.json()

    email = info.get("email", "")
    if not email:
        return RedirectResponse(url="/login?error=google_email", status_code=302)
    user = await auth_service.create_or_get_user(
        db, email, info.get("name", ""), "google", str(info.get("sub", ""))
    )
    user.picture_url = info.get("picture")
    return await _finish_login(request, db, user)


@router.get("/facebook")
async def facebook_login(request: Request):
    if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET:
        return RedirectResponse(url="/login?error=facebook_not_configured", status_code=302)
    from urllib.parse import urlencode

    params = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
        "scope": "email",
        "response_type": "code",
    }
    return RedirectResponse(
        "https://www.facebook.com/v18.0/dialog/oauth?" + urlencode(params), status_code=302
    )


@router.get("/facebook/callback")
async def facebook_callback(code: str, request: Request, db: AsyncSession = Depends(get_session)):
    if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET:
        return RedirectResponse(url="/login?error=facebook_not_configured", status_code=302)
    import httpx

    async with httpx.AsyncClient(timeout=15) as client:
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
        access = token_data.get("access_token")
        if not access:
            return RedirectResponse(url="/login?error=facebook_token", status_code=302)
        info_res = await client.get(
            "https://graph.facebook.com/me",
            params={"fields": "id,name,email,picture", "access_token": access},
        )
        info = info_res.json()

    email = info.get("email", "")
    if not email:
        return RedirectResponse(url="/login?error=facebook_email", status_code=302)
    user = await auth_service.create_or_get_user(
        db, email, info.get("name", ""), "facebook", str(info.get("id", ""))
    )
    return await _finish_login(request, db, user)


@router.post("/magic/send")
@limiter.limit("5/minute")
async def magic_send(
    request: Request,
    email: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    email = email.strip().lower()
    if "@" not in email:
        return RedirectResponse(url="/login?error=email", status_code=302)
    user = await auth_service.create_or_get_user(db, email, "", "email_link", "")
    token = await auth_service.issue_magic_token(db, user, security.client_ip(request))
    msg = "Check your email for a sign-in link."
    dev = None
    if not auth_service._smtp_configured():
        # Dev fallback: expose the link so the flow is testable without SMTP.
        dev = f"{settings.FRONTEND_BASE_URL}/auth/magic/verify?token={token}"
        msg = "SMTP is not configured. Use the development link below."
    return JSONResponse({"ok": True, "sent": True, "message": msg, "dev_link": dev})


@router.get("/magic/verify")
async def magic_verify(
    token: str,
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    user = await auth_service.consume_magic_token(db, token)
    if user is None:
        return RedirectResponse(url="/login?error=magic_expired", status_code=302)
    return await _finish_login(request, db, user)


@router.post("/admin/login")
@limiter.limit("10/minute")
async def admin_login(
    request: Request,
    password: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    admin = await auth_service.bootstrap_admin(db)
    if admin is None or not admin.hashed_password or not security.verify_password(password, admin.hashed_password):
        return RedirectResponse(url="/admin?error=1", status_code=302)
    return await _finish_login(request, db, admin)


@router.get("/me")
async def me(request: Request, db: AsyncSession = Depends(get_session)):
    from app.deps import get_current_user

    user = await get_current_user(request, db)
    if user is None:
        return JSONResponse({"authenticated": False}, status_code=200)
    return {"authenticated": True, "user": user.public_dict()}


@router.post("/logout")
@router.get("/logout")
async def logout(request: Request, db: AsyncSession = Depends(get_session)):
    token = request.cookies.get(security.SESSION_COOKIE)
    if token:
        await auth_service.revoke_session(db, token)
    resp = RedirectResponse(url="/", status_code=302)
    resp.delete_cookie(security.SESSION_COOKIE, path="/")
    return resp