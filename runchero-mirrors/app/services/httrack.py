"""HTTrack job runner."""
from __future__ import annotations

import os
import re
import signal
import subprocess
import threading
import time
from pathlib import Path

from .. import config, db


_lock = threading.Lock()
_running = {}


def _slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return s or "site"


def _parse_stats(line: str):
    # Try to extract rough stats from httrack output if possible
    # common patterns vary; we store raw lines too
    return None


def start_mirror(conn, mirror_id: int, speed: str = "slow"):
    with _lock:
        if mirror_id in _running:
            return False
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return False
    if row["status"] not in ("queued", "paused"):
        # allow restarting if marked queued? be permissive
        pass

    mirror = dict(row)
    outdir = Path(mirror["output_dir"])
    outdir.mkdir(parents=True, exist_ok=True)

    # Build httrack command - simple, gentle defaults for community use
    url = mirror["url"].strip()
    if not url:
        conn.execute("UPDATE mirrors SET status='failed', error_log='No URL provided', updated_at=datetime('now') WHERE id=?", (mirror_id,))
        conn.commit()
        return False

    # Use httrack with reasonable defaults; can be tuned
    env = os.environ.copy()
    if config.HTTRACK_LIB:
        env["LD_LIBRARY_PATH"] = config.HTTRACK_LIB + ":" + env.get("LD_LIBRARY_PATH", "")

    # Command: httrack <url> -O <path> +* -v (gentle defaults)
    speed = (speed or "slow").lower()
    if speed == "very-slow":
        cmd = [config.HTTRACK_BIN, url, "-O", str(outdir), "+*", "-r4", "-c2", "--rate=200", "-v"]
    elif speed == "medium":
        cmd = [config.HTTRACK_BIN, url, "-O", str(outdir), "+*", "-r5", "-c4", "--rate=1000", "-v"]
    else:  # slow/default
        cmd = [config.HTTRACK_BIN, url, "-O", str(outdir), "+*", "-r4", "-c1", "--rate=100", "-v"]
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(outdir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            preexec_fn=os.setsid if os.name != "nt" else None,
        )
    except Exception as e:
        conn.execute("UPDATE mirrors SET status='failed', error_log=?, updated_at=datetime('now') WHERE id=?", (str(e), mirror_id))
        conn.commit()
        return False

    conn.execute("UPDATE mirrors SET status='running', pid=?, started_at=COALESCE(started_at, datetime('now')), updated_at=datetime('now') WHERE id=?", (proc.pid, mirror_id))
    conn.commit()

    t = threading.Thread(target=_watch, args=(mirror_id, proc), daemon=True)
    with _lock:
        _running[mirror_id] = proc
    t.start()
    return True


def stop_mirror(conn, mirror_id: int):
    with _lock:
        proc = _running.get(mirror_id)
    if not proc:
        row = db.one(conn, "SELECT pid FROM mirrors WHERE id=?", (mirror_id,))
        if row and row["pid"]:
            try:
                os.killpg(os.getpgid(int(row["pid"])), signal.SIGTERM)
            except Exception:
                try:
                    os.kill(int(row["pid"]), signal.SIGTERM)
                except Exception:
                    pass
    else:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            try:
                proc.terminate()
            except Exception:
                pass
    conn.execute("UPDATE mirrors SET status='cancelled', updated_at=datetime('now'), finished_at=datetime('now') WHERE id=?", (mirror_id,))
    conn.commit()
    return True


def _watch(mirror_id: int, proc: subprocess.Popen):
    conn = db.connect()
    try:
        db.init_db(conn)
        pages = files = bytes_saved = 0
        for line in proc.stdout:
            try:
                s = line.decode('utf-8', errors='replace').rstrip()
            except Exception:
                continue
            if not s:
                continue
            try:
                conn.execute("INSERT INTO mirror_logs(mirror_id, line) VALUES(?,?)", (mirror_id, s))
                # crude parsing
                # look for counts if present
                m = re.search(r'(\d+)\s+files?', s, re.I)
                if m:
                    files = max(files, int(m.group(1)))
                m2 = re.search(r'(\d+)\s+links?', s, re.I)
                if m2:
                    pages = max(pages, int(m2.group(1)))
            except Exception:
                pass
            try:
                conn.execute("INSERT OR REPLACE INTO mirror_stats(mirror_id,pages_saved,files_saved,bytes_saved,links_processed,errors_count,updated_at) VALUES(?,?,?,?,?,?,datetime('now'))",
                             (mirror_id, pages, files, bytes_saved, pages, 0))
                conn.execute("UPDATE mirrors SET updated_at=datetime('now') WHERE id=?", (mirror_id,))
                conn.commit()
            except Exception:
                pass
        rc = proc.wait()
        try:
            if rc == 0:
                conn.execute("UPDATE mirrors SET status='completed', finished_at=datetime('now'), updated_at=datetime('now') WHERE id=?", (mirror_id,))
            else:
                row = db.one(conn, "SELECT error_log FROM mirrors WHERE id=?", (mirror_id,))
                err = (row['error_log'] if row else '') + f"\n[exit {rc}]"
                conn.execute("UPDATE mirrors SET status='failed', finished_at=datetime('now'), updated_at=datetime('now'), error_log=? WHERE id=?", (err[-8000:], mirror_id))
            conn.commit()
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass
        with _lock:
            _running.pop(mirror_id, None)


def get_running():
    with _lock:
        return dict(_running)
