"""Helpers for saving uploaded images."""
from __future__ import annotations

import io
import re
import uuid
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from .. import config

MAX_BYTES = 2 * 1024 * 1024
MAX_PIXELS = 20_000_000


def save_upload(store_slug: str, field: dict, slug_hint: str = "") -> str:
    """Persist an uploaded file; return its /static/... URL or '' on failure."""
    if not re.fullmatch(r"[a-z0-9-]{1,40}", store_slug):
        return ""
    if not field or not field.get("data"):
        return ""
    data = field["data"]
    if len(data) > MAX_BYTES:
        return ""
    if not isinstance(data, bytes):
        return ""
    try:
        with Image.open(io.BytesIO(data)) as source:
            if source.width * source.height > MAX_PIXELS:
                return ""
            source.verify()
        with Image.open(io.BytesIO(data)) as source:
            image = ImageOps.exif_transpose(source).convert("RGBA")
            image.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
            output = io.BytesIO()
            image.save(output, format="PNG", optimize=True)
            data = output.getvalue()
    except (UnidentifiedImageError, OSError, ValueError):
        return ""
    if len(data) > MAX_BYTES * 2:
        return ""
    target_dir = config.STATIC_DIR / "img" / "uploads" / store_slug
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_hint = re.sub(r"[^a-zA-Z0-9-]+", "-", slug_hint).strip("-")[:48]
    name = (safe_hint or "img") + "-" + uuid.uuid4().hex[:8] + ".png"
    path = target_dir / name
    path.write_bytes(data)
    return "/static/img/uploads/" + store_slug + "/" + name
