"""FastAPI application factory: middleware, security headers, routers, static."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.api import auth_router, offers, tracking
from app.config import settings
from app.db import init_db
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
            "script-src 'self' https://maps.googleapis.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


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

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Mount static
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# Routers
app.include_router(auth_router.router)
app.include_router(offers.router)
app.include_router(tracking.router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"ok": True, "version": settings.VERSION, "name": settings.PROJECT_NAME}


@app.get("/robots.txt")
async def robots():
    return HTMLResponse(
        "User-agent: *\nAllow: /\nDisallow: /admin/\n",
        media_type="text/plain",
    )