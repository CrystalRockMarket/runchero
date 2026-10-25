#!/usr/bin/env python3
"""Set, check or clear the admin password stored in the depot database.

    python3 tools/admin_password.py set
    python3 tools/admin_password.py set --password 'long temporary password'
    python3 tools/admin_password.py status
    python3 tools/admin_password.py clear
"""
from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import admin, db  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["set", "status", "clear"])
    parser.add_argument("--password", help="non-interactive password (8+ chars)")
    args = parser.parse_args(argv)

    conn = db.connect()
    db.init_db(conn)
    try:
        if args.action == "status":
            print("configured" if admin.configured(conn) else "not configured")
            return 0
        if args.action == "clear":
            conn.execute("DELETE FROM meta WHERE key='admin_password_hash'")
            conn.commit()
            print("admin password cleared")
            return 0
        password = args.password
        if password is None:
            password = getpass.getpass("New admin password: ")
            again = getpass.getpass("Repeat: ")
            if password != again:
                print("passwords do not match", file=sys.stderr)
                return 2
        admin.set_password(conn, password)
        print("admin password set")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
