"""Admin passwords: PBKDF2 hashing and first-boot owner creation."""
from __future__ import annotations

import hashlib
import secrets

from .. import db, config

_PBKDF2_ITERATIONS = 240_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt,
                                 _PBKDF2_ITERATIONS)
    return f"pbkdf2${_PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def check_password(password: str, stored: str) -> bool:
    try:
        _, iterations, salt, digest = stored.split("$")
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt),
            int(iterations))
        return secrets.compare_digest(candidate.hex(), digest)
    except (ValueError, TypeError):
        return False


def ensure_admin(conn: db.sqlite3.Connection) -> str | None:
    """Create the owner account from the environment on first boot.

    Without environment credentials a demo owner is created with a password
    printed once to the seed report, so the console is reachable but the
    password is not a permanent default.
    """
    username = config.ADMIN_USER or "runchero"
    password = config.ADMIN_PASSWORD or ""
    generated = None
    if not password:
        row = db.one(conn, "SELECT id FROM admins WHERE username = ?",
                    (username,))
        if row is not None:
            return None
        password = generated = f"demo-{secrets.token_hex(4)}"
    row = db.one(conn, "SELECT id FROM admins WHERE username = ?",
                 (username,))
    if row is None:
        conn.execute("INSERT INTO admins(username, passhash, role) "
                     "VALUES(?, ?, 'owner')",
                     (username, hash_password(password)))
        conn.commit()
    return generated
