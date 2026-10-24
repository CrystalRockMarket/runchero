"""HTTrack process management and progress tracking."""
from __future__ import annotations

import datetime as dt
import os
import re
import shutil
import signal
import subprocess
import threading
import time
import traceback
from pathlib import Path
from urllib.parse import unquote, urlparse

from .. import config, crawl_options, db

_lock = threading.Lock()
_active: dict[int, subprocess.Popen] = {}
_worker: threading.Thread | None = None

PAGE_SUFFIXES = {
    ".html", ".htm", ".xhtml", ".shtml",
    ".php", ".asp", ".aspx", ".jsp", ".cgi", ".pl",
}
INDEX_NAMES = (
    "index.html", "index.htm", "index.xhtml", "index.shtml",
    "index.php", "index.asp", "index.aspx", "index.jsp",
)


def looks_like_html(path: Path) -> bool:
    try:
        with open(path, "rb") as handle:
            head = handle.read(4096).lower()
    except OSError:
        return False
    return any(marker in head for marker in (b"<html", b"<!doctype html", b"<head", b"<body"))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def available() -> bool:
    return bool(config.HTTRACK_BIN) and os.path.isfile(config.HTTRACK_BIN) and os.access(
        config.HTTRACK_BIN, os.X_OK
    )


def _now() -> str:
    return dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _clock(value: float) -> str:
    # Database timestamps are UTC; keep file mtimes in the same frame.
    return dt.datetime.utcfromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")


def _mirror_dir(row) -> Path:
    return Path(row["output_dir"])


def _cache_dir(row) -> Path:
    return config.MIRRORS_ROOT / ".cache" / row["slug"]


def log_path(row) -> Path:
    return config.MIRRORS_ROOT / ".cache" / f"{row['slug']}.log"


def _kill_group(pid: int | None, sig: int) -> None:
    if not pid:
        return
    try:
        os.killpg(int(pid), sig)
    except (ProcessLookupError, PermissionError):
        pass
    except OSError:
        try:
            os.kill(int(pid), sig)
        except OSError:
            pass


def _pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except OSError:
        return False


def _pid_is_httrack(pid: int | None) -> bool:
    """Guard against recycled PIDs when cleaning up after a restart."""
    if not pid:
        return False
    try:
        raw = Path(f"/proc/{int(pid)}/cmdline").read_bytes()
    except OSError:
        return False
    return b"httrack" in raw.lower()


def _scan_tree(root: Path) -> tuple[int, int, int, str | None]:
    """Return (pages, files, bytes, newest_file_time)."""
    pages = files = total = 0
    newest: float | None = None
    if not root.exists():
        return 0, 0, 0, None
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name for name in dirnames
            if name not in {"hts-cache", ".cache"} and not name.startswith(".")
        ]
        for name in filenames:
            if name.startswith("."):
                continue
            path = Path(dirpath) / name
            try:
                stat = path.stat()
            except OSError:
                continue
            files += 1
            total += stat.st_size
            if stat.st_mtime > (newest or 0):
                newest = stat.st_mtime
            # HTTrack writes unfinished pages as name.html.tmp and only renames
            # them when the download is complete. Count those as pages now so
            # the progress panel is honest during a crawl.
            real_name = name[:-4] if name.lower().endswith(".tmp") else name
            if Path(real_name).suffix.lower() in PAGE_SUFFIXES:
                pages += 1
    return pages, files, total, _clock(newest) if newest else None


def _candidate_entries(root: Path, source_url: str) -> list[Path]:
    """Find HTML files that could be the front door of the mirror."""
    parsed = urlparse(source_url)
    host = (parsed.netloc or "").lower()
    lookup = unquote(parsed.path or "/")
    if lookup == "":
        lookup = "/"
    rel = lookup.lstrip("/")
    hosts = []
    if host:
        hosts.append(root / host)
        hosts.append(root / host.replace(":", "_"))
    found: list[Path] = []
    candidates: list[Path] = []
    for host_dir in hosts:
        if rel.endswith("/") or rel == "":
            for index_name in INDEX_NAMES:
                candidates.append(host_dir / rel / index_name)
        else:
            candidates.append(host_dir / rel)
            for index_name in INDEX_NAMES:
                candidates.append(host_dir / rel / index_name)
            candidates.append(host_dir / (rel + ".html"))
    candidates.append(root / rel)
    for index_name in INDEX_NAMES:
        candidates.append(root / rel / index_name)
    candidates.append(root / (rel + ".html"))
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
            candidate.relative_to(root.resolve())
        except (OSError, ValueError):
            continue
        if candidate.is_file() and (
            candidate.suffix.lower() in PAGE_SUFFIXES or looks_like_html(candidate)
        ):
            found.append(candidate)

    if found:
        return found

    html_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name for name in dirnames
            if name not in {"hts-cache", ".cache"} and not name.startswith(".")
        ]
        for name in filenames:
            suffix = Path(name).suffix.lower()
            if suffix in PAGE_SUFFIXES:
                html_files.append(Path(dirpath) / name)

    def score(path: Path):
        try:
            relative = path.relative_to(root)
        except ValueError:
            relative = path
        index_rank = 0 if path.name.lower() in INDEX_NAMES else 1
        path_rank = 0
        if rel:
            if relative.as_posix().endswith(rel.rstrip("/") + "/index.html"):
                path_rank = 0
            elif rel.rstrip("/") in relative.as_posix():
                path_rank = 1
            else:
                path_rank = 2
        return (index_rank, path_rank, len(relative.parts), relative.as_posix())

    return sorted(html_files, key=score)


def find_entry(root: Path, source_url: str) -> tuple[str, str]:
    """Return (entry_path, serve_root), both relative to the mirror root."""
    root = root.resolve()
    for candidate in _candidate_entries(root, source_url):
        try:
            relative = candidate.resolve().relative_to(root)
        except ValueError:
            continue
        serve_root = relative.parent
        return relative.as_posix(), serve_root.as_posix()
    return "", ""


_ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_ANSI_OSC = re.compile(r"\x1b\][^\x07]*(?:\x07|\x1b\\)")


def clean_log(text: str) -> str:
    text = _ANSI_OSC.sub("", text)
    text = _ANSI.sub("", text)
    text = text.replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line.strip())


def read_log(row, max_bytes: int = 400_000) -> str:
    path = log_path(row)
    try:
        with open(path, "rb") as handle:
            handle.seek(0, 2)
            size = handle.tell()
            handle.seek(max(0, size - max_bytes))
            data = handle.read()
    except OSError:
        return ""
    return clean_log(data.decode("utf-8", "replace"))


def _tail(path: Path, lines: int = 60) -> str:
    try:
        text = clean_log(path.read_text("utf-8", errors="replace"))
        data = text.splitlines()
        return "\n".join(data[-lines:])[-12000:]
    except OSError:
        return ""


# --------------------------------------------------------------------------
# lifecycle
# --------------------------------------------------------------------------

def recover(conn) -> None:
    """Close out jobs left running by a previous server process."""
    stale = db.rows(
        conn,
        "SELECT * FROM mirrors WHERE status IN ('running', 'paused', 'starting')",
    )
    for row in stale:
        if _pid_is_httrack(row["pid"]):
            _kill_group(row["pid"], signal.SIGCONT)
            _kill_group(row["pid"], signal.SIGTERM)
        conn.execute(
            "UPDATE mirrors SET status='failed', pid=NULL, finished_at=?, "
            "updated_at=?, error_log=CASE WHEN error_log='' THEN ? ELSE error_log END "
            "WHERE id=?",
            (_now(), _now(), "The depot restarted while this download was running. Retry it.", row["id"]),
        )
    conn.commit()


def ensure_worker() -> None:
    global _worker
    with _lock:
        if _worker is not None and _worker.is_alive():
            return
        _worker = threading.Thread(target=_queue_loop, name="mirror-queue", daemon=True)
        _worker.start()


def _active_count() -> int:
    with _lock:
        return len(_active)


def _queue_loop() -> None:
    while True:
        conn = None
        try:
            if _active_count() < config.MAX_CONCURRENT:
                conn = db.connect()
                row = db.one(
                    conn,
                    "SELECT * FROM mirrors WHERE status='queued' "
                    "ORDER BY created_at ASC, id ASC LIMIT 1",
                )
                if row is not None:
                    claimed = conn.execute(
                        "UPDATE mirrors SET status='starting', updated_at=? "
                        "WHERE id=? AND status='queued'",
                        (_now(), row["id"]),
                    )
                    conn.commit()
                    if claimed.rowcount == 1:
                        try:
                            start_process(conn, row)
                        except Exception as exc:
                            traceback.print_exc()
                            conn.execute(
                                "UPDATE mirrors SET status='failed', pid=NULL, updated_at=?, "
                                "error_log=? WHERE id=? AND status='starting'",
                                (_now(), f"Could not start the crawl: {exc}", row["id"]),
                            )
                            conn.commit()
        except Exception:
            traceback.print_exc()
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
        time.sleep(1.0)


def start_process(conn, row) -> bool:
    mirror_id = int(row["id"])
    fresh = db.one(conn, "SELECT status, cancel_requested FROM mirrors WHERE id=?", (mirror_id,))
    if not fresh or fresh["status"] != "starting" or fresh["cancel_requested"]:
        return False
    if not available():
        conn.execute(
            "UPDATE mirrors SET status='failed', finished_at=?, updated_at=?, "
            "error_log='The HTTrack website copier is not installed. Ask an administrator to check the app.' "
            "WHERE id=?",
            (_now(), _now(), mirror_id),
        )
        conn.commit()
        return False

    speed = row["speed"] or config.DEFAULT_SPEED
    options = crawl_options.resolve(speed, row["options_json"])
    keep_existing = bool(options["keep_existing"])
    outdir = _mirror_dir(row)
    cache = _cache_dir(row)
    logfile = log_path(row)

    if not keep_existing:
        for folder in (outdir, cache):
            try:
                if folder.exists():
                    shutil.rmtree(folder)
            except OSError as exc:
                conn.execute(
                    "UPDATE mirrors SET status='failed', updated_at=?, error_log=? WHERE id=?",
                    (_now(), f"Could not prepare the mirror folder: {exc}", mirror_id),
                )
                conn.commit()
                return False
    outdir.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)
    logfile.parent.mkdir(parents=True, exist_ok=True)

    scope = "--stay-on-same-domain" if options["scope"] == "domain" else "--stay-on-same-address"
    cmd = [
        config.HTTRACK_BIN,
        row["url"],
        "-O", f"{outdir},{cache}",
        f"--sockets={int(options['sockets'])}",
        f"--max-rate={int(options['rate'])}",
        f"--depth={int(options['depth'])}",
        f"--max-size={int(options['max_bytes'])}",
        f"--max-time={int(options['max_seconds'])}",
        f"--timeout={int(options['timeout'])}",
        f"--retries={int(options['retries'])}",
        "--connection-per-second=1",
        f"--robots={int(options['robots'])}",
        "--near",
        scope,
        f"--user-agent={config.USER_AGENT}",
        "--quiet",
        "--display=1",
        "-I0",
    ]
    if keep_existing:
        cmd.insert(2, "--continue")
    env = os.environ.copy()
    if config.HTTRACK_LIB:
        env["LD_LIBRARY_PATH"] = config.HTTRACK_LIB + ":" + env.get("LD_LIBRARY_PATH", "")

    started = _now()
    prepared = conn.execute(
        "UPDATE mirrors SET status='starting', pid=NULL, speed=?, started_at=?, "
        "finished_at=NULL, entry_path='', serve_root='', "
        "last_activity=NULL, updated_at=?, error_log='' "
        "WHERE id=? AND status='starting' AND cancel_requested=0",
        (speed, started, started, mirror_id),
    )
    conn.commit()
    if prepared.rowcount != 1:
        return False
    conn.execute(
        "INSERT INTO mirror_stats(mirror_id, pages_saved, files_saved, bytes_saved, "
        "links_processed, errors_count, rate_bps, updated_at) "
        "VALUES(?, 0, 0, 0, 0, 0, 0, ?) "
        "ON CONFLICT(mirror_id) DO UPDATE SET pages_saved=0, files_saved=0, "
        "bytes_saved=0, links_processed=0, errors_count=0, rate_bps=0, updated_at=excluded.updated_at",
        (mirror_id, started),
    )
    conn.commit()

    log_handle = None
    try:
        log_handle = open(logfile, "wb")
        log_handle.write(f"Runchero Mirrors crawl started {started} UTC\n".encode())
        log_handle.write(
            (
                f"Source: {row['url']}\n"
                f"Speed: {speed} · depth {options['depth']} · "
                f"{max(1, round(options['rate'] / 1000))} KB/s · "
                f"{options['sockets']} connection(s)\n"
                f"Limits: {options['max_bytes'] / 1_000_000:g} MB, "
                f"{options['max_seconds'] / 3600:g} hours · scope {options['scope']}\n\n"
            ).encode()
        )
        log_handle.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=str(outdir),
            stdin=subprocess.DEVNULL,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,
        )
    except Exception as exc:
        try:
            if log_handle:
                log_handle.close()
        except Exception:
            pass
        conn.execute(
            "UPDATE mirrors SET status='failed', finished_at=?, updated_at=?, error_log=? WHERE id=?",
            (_now(), _now(), f"Could not start HTTrack: {exc}", mirror_id),
        )
        conn.commit()
        return False

    try:
        log_handle.close()
    except Exception:
        pass

    claimed = conn.execute(
        "UPDATE mirrors SET status='running', pid=?, updated_at=? "
        "WHERE id=? AND status='starting' AND cancel_requested=0",
        (proc.pid, _now(), mirror_id),
    )
    conn.commit()
    if claimed.rowcount != 1:
        _kill_group(proc.pid, signal.SIGCONT)
        _kill_group(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _kill_group(proc.pid, signal.SIGKILL)
        conn.execute(
            "UPDATE mirrors SET status='cancelled', pid=NULL, finished_at=?, updated_at=? "
            "WHERE id=? AND status IN ('starting','running')",
            (_now(), _now(), mirror_id),
        )
        conn.commit()
        return False
    with _lock:
        _active[mirror_id] = proc
    watcher = threading.Thread(
        target=_monitor,
        args=(mirror_id, proc, outdir),
        name=f"mirror-{mirror_id}",
        daemon=True,
    )
    watcher.start()
    return True


# --------------------------------------------------------------------------
# monitoring
# --------------------------------------------------------------------------

def _monitor(mirror_id: int, proc: subprocess.Popen, outdir: Path) -> None:
    conn = None
    last_bytes = 0
    last_time = time.monotonic()
    try:
        conn = db.connect()
        db.init_db(conn)
        last_scan = 0.0
        while True:
            rc = proc.poll()
            status = db.scalar(conn, "SELECT status FROM mirrors WHERE id=?", (mirror_id,))
            now_mono = time.monotonic()
            if rc is None and now_mono - last_scan >= 2.0:
                pages, files, total, newest = _scan_tree(outdir)
                elapsed = max(0.001, now_mono - last_time)
                rate = max(0, int((total - last_bytes) / elapsed))
                if status == "paused":
                    rate = 0
                conn.execute(
                    "INSERT INTO mirror_stats(mirror_id, pages_saved, files_saved, bytes_saved, "
                    "links_processed, errors_count, rate_bps, updated_at) "
                    "VALUES(?, ?, ?, ?, ?, 0, ?, ?) "
                    "ON CONFLICT(mirror_id) DO UPDATE SET pages_saved=excluded.pages_saved, "
                    "files_saved=excluded.files_saved, bytes_saved=excluded.bytes_saved, "
                    "rate_bps=excluded.rate_bps, updated_at=excluded.updated_at",
                    (mirror_id, pages, files, total, pages, rate, _now()),
                )
                conn.execute(
                    "UPDATE mirrors SET last_activity=?, updated_at=? WHERE id=?",
                    (newest, _now(), mirror_id),
                )
                conn.commit()
                last_bytes = total
                last_time = now_mono
                last_scan = now_mono
            if rc is not None:
                break
            if status == "cancelled":
                _kill_group(proc.pid, signal.SIGCONT)
                _kill_group(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    _kill_group(proc.pid, signal.SIGKILL)
                break
            time.sleep(0.5)

        # Final state. The row may have been cancelled by a button while the
        # process was finishing, so always re-read it before deciding.
        row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
        if row is None:
            return
        pages, files, total, newest = _scan_tree(outdir)
        status = row["status"]
        if status == "cancelled":
            final_status = "cancelled"
            error = row["error_log"]
        else:
            entry, serve_root = find_entry(outdir, row["url"])
            if pages > 0 and entry:
                final_status = "completed"
                error = "" if proc.returncode == 0 else _tail(log_path(row), 20)
            else:
                final_status = "failed"
                error = (
                    "No pages were saved. Check that the web address is correct and "
                    "that the site is reachable from this computer."
                )
                technical = _tail(log_path(row), 25)
                if technical:
                    error += "\n\n" + technical
        conn.execute(
            "INSERT INTO mirror_stats(mirror_id, pages_saved, files_saved, bytes_saved, "
            "links_processed, errors_count, rate_bps, updated_at) "
            "VALUES(?, ?, ?, ?, ?, 0, 0, ?) "
            "ON CONFLICT(mirror_id) DO UPDATE SET pages_saved=excluded.pages_saved, "
            "files_saved=excluded.files_saved, bytes_saved=excluded.bytes_saved, "
            "rate_bps=0, updated_at=excluded.updated_at",
            (mirror_id, pages, files, total, pages, _now()),
        )
        if final_status == "completed":
            conn.execute(
                "UPDATE mirrors SET status='completed', pid=NULL, finished_at=?, "
                "updated_at=?, last_activity=?, entry_path=?, serve_root=?, "
                "error_log=? WHERE id=?",
                (_now(), _now(), newest, entry, serve_root, error, mirror_id),
            )
        elif final_status == "failed":
            conn.execute(
                "UPDATE mirrors SET status='failed', pid=NULL, finished_at=?, "
                "updated_at=?, last_activity=?, error_log=? WHERE id=?",
                (_now(), _now(), newest, error, mirror_id),
            )
        else:
            conn.execute(
                "UPDATE mirrors SET status='cancelled', pid=NULL, finished_at=?, "
                "updated_at=?, last_activity=? WHERE id=?",
                (_now(), _now(), newest, mirror_id),
            )
        conn.commit()
    except Exception:
        traceback.print_exc()
        try:
            _kill_group(proc.pid, signal.SIGTERM)
        except Exception:
            pass
        if conn is not None:
            try:
                conn.execute(
                    "UPDATE mirrors SET status='failed', pid=NULL, finished_at=?, updated_at=?, "
                    "error_log=? WHERE id=?",
                    (_now(), _now(), "The download watcher hit an error. See the depot log.", mirror_id),
                )
                conn.commit()
            except Exception:
                pass
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        with _lock:
            _active.pop(mirror_id, None)


# --------------------------------------------------------------------------
# user actions
# --------------------------------------------------------------------------

def enqueue(conn, mirror_id: int) -> None:
    conn.execute(
        "UPDATE mirrors SET status='queued', cancel_requested=0, updated_at=? WHERE id=?",
        (_now(), mirror_id),
    )
    conn.commit()
    ensure_worker()


def retry(conn, mirror_id: int) -> bool:
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row or row["status"] not in ("failed", "cancelled"):
        return False
    conn.execute(
        "UPDATE mirrors SET status='queued', pid=NULL, cancel_requested=0, "
        "entry_path='', serve_root='', started_at=NULL, finished_at=NULL, "
        "last_activity=NULL, error_log='', updated_at=? WHERE id=?",
        (_now(), mirror_id),
    )
    conn.commit()
    ensure_worker()
    return True


def rerun(conn, mirror_id: int, speed: str, options_json: str) -> tuple[bool, str]:
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return False, "That mirror was not found."
    if row["status"] not in ("completed", "failed", "cancelled"):
        return False, "That site is still working. Stop it before rerunning."
    changed = conn.execute(
        "UPDATE mirrors SET status='queued', speed=?, options_json=?, pid=NULL, "
        "cancel_requested=0, entry_path='', serve_root='', started_at=NULL, "
        "finished_at=NULL, last_activity=NULL, error_log='', updated_at=? "
        "WHERE id=? AND status IN ('completed','failed','cancelled')",
        (speed, options_json, _now(), mirror_id),
    )
    conn.commit()
    if changed.rowcount != 1:
        return False, "That mirror changed before it could be rerun. Please try again."
    ensure_worker()
    return True, "Queued for another try."


def pause(conn, mirror_id: int) -> tuple[bool, str]:
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return False, "That mirror was not found."
    if row["status"] != "running":
        return False, "That site is not currently downloading."
    pid = row["pid"]
    with _lock:
        proc = _active.get(mirror_id)
        if proc is not None:
            pid = proc.pid
    if not _pid_alive(pid):
        return False, "The download process is no longer running. It may have just finished."
    _kill_group(pid, signal.SIGSTOP)
    conn.execute(
        "UPDATE mirrors SET status='paused', updated_at=? WHERE id=?",
        (_now(), mirror_id),
    )
    conn.commit()
    return True, "Paused. Click Resume when you are ready."


def resume(conn, mirror_id: int) -> tuple[bool, str]:
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return False, "That mirror was not found."
    if row["status"] != "paused":
        return False, "That site is not paused."
    pid = row["pid"]
    with _lock:
        proc = _active.get(mirror_id)
        if proc is not None:
            pid = proc.pid
    if not _pid_alive(pid):
        return False, "The paused process is gone. Stop and retry this site."
    _kill_group(pid, signal.SIGCONT)
    conn.execute(
        "UPDATE mirrors SET status='running', updated_at=? WHERE id=?",
        (_now(), mirror_id),
    )
    conn.commit()
    return True, "Downloading again."


def cancel(conn, mirror_id: int) -> tuple[bool, str]:
    row = db.one(conn, "SELECT * FROM mirrors WHERE id=?", (mirror_id,))
    if not row:
        return False, "That mirror was not found."
    if row["status"] in ("completed", "cancelled"):
        return False, "That download is already finished."
    pid = row["pid"]
    with _lock:
        proc = _active.get(mirror_id)
        if proc is not None:
            pid = proc.pid
    if row["status"] == "paused":
        _kill_group(pid, signal.SIGCONT)
    _kill_group(pid, signal.SIGTERM)
    conn.execute(
        "UPDATE mirrors SET status='cancelled', cancel_requested=1, finished_at=?, "
        "updated_at=? WHERE id=?",
        (_now(), _now(), mirror_id),
    )
    conn.commit()
    return True, "Stopped. The partial copy is kept out of the finished browse page."


def shutdown() -> None:
    with _lock:
        procs = list(_active.items())
    for mirror_id, proc in procs:
        _kill_group(proc.pid, signal.SIGCONT)
        _kill_group(proc.pid, signal.SIGTERM)
    for mirror_id, proc in procs:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _kill_group(proc.pid, signal.SIGKILL)
    if procs:
        try:
            with db.session() as conn:
                for mirror_id, _proc in procs:
                    conn.execute(
                        "UPDATE mirrors SET status='failed', pid=NULL, finished_at=?, updated_at=?, "
                        "error_log=CASE WHEN error_log='' THEN ? ELSE error_log END WHERE id=? "
                        "AND status IN ('running','paused','starting')",
                        (_now(), _now(), "The depot was shut down during this download. Retry it.", mirror_id),
                    )
        except Exception:
            traceback.print_exc()
