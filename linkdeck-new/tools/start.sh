#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Prefer the project venv if present.
if [ -x "$ROOT/venv/bin/python" ]; then
    PY="$ROOT/venv/bin/python"
else
    PY="$(command -v python3)"
fi

PIDFILE="${LD_PID_PATH:-/home/barn/run/linkdeck.pid}"
LOGFILE="${LD_LOG_PATH:-/home/barn/logs/linkdeck.log}"
HOST="${LD_HOST:-0.0.0.0}"
PORT="${LD_PORT:-8092}"

mkdir -p "$(dirname "$PIDFILE")" "$(dirname "$LOGFILE")"

running() {
    [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null
}

ensure_deps() {
    if ! "$PY" -c "import fastapi, uvicorn, sqlalchemy, bcrypt" >/dev/null 2>&1; then
        echo "installing dependencies into $PY ..."
        "$PY" -m pip install -q -r "$ROOT/requirements.txt"
    fi
}

start() {
    if running; then echo "already running (pid $(cat "$PIDFILE"))"; return 0; fi
    ensure_deps
    cd "$ROOT" || exit 1
    rm -f "$PIDFILE"
    setsid nohup "$PY" -m uvicorn app.httpd:app --host "$HOST" --port "$PORT" \
        >>"$LOGFILE" 2>&1 < /dev/null &
    echo $! > "$PIDFILE"
    for _ in $(seq 1 50); do
        if running; then echo "started on http://$HOST:$PORT (pid $(cat "$PIDFILE"))"; return 0; fi
        sleep 0.2
    done
    echo "failed to start; see $LOGFILE"; tail -10 "$LOGFILE"; rm -f "$PIDFILE"; return 1
}

stop() {
    if running; then
        local pid
        pid="$(cat "$PIDFILE")"
        kill "$pid" 2>/dev/null || true
        for _ in $(seq 1 80); do
            kill -0 "$pid" 2>/dev/null || break
            sleep 0.25
        done
        if kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null || true
        fi
    fi
    rm -f "$PIDFILE"
}

status() {
    if running; then echo "running (pid $(cat "$PIDFILE"))"; else echo "stopped"; fi
}

case "${1:-start}" in
    start) start ;;
    stop)  stop ;;
    restart) stop; start ;;
    status) status ;;
    *) echo "Usage: $0 {start|stop|restart|status}" >&2; exit 1 ;;
esac