#!/usr/bin/env bash
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE="${RDIR_PID_PATH:-/home/barn/run/runchero-community.pid}"
LOGFILE="${RDIR_LOG_PATH:-/home/barn/logs/runchero-community.log}"
HOST="${RDIR_HOST:-0.0.0.0}"
PORT="${RDIR_PORT:-8093}"
PY="${PYTHON:-/usr/bin/python3}"
DB="${RDIR_DB_PATH:-/home/barn/data/runchero-community.db}"
BACKUP_DIR="${RDIR_BACKUP_DIR:-/home/barn/data/backups}"
mkdir -p "$(dirname "$PIDFILE")" "$(dirname "$LOGFILE")"
running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }
start() {
  if running; then echo "already running (pid $(cat "$PIDFILE"))"; return 0; fi
  cd "$ROOT" || exit 1
  rm -f "$PIDFILE"
  setsid nohup "$PY" run.py --host "$HOST" --port "$PORT" >>"$LOGFILE" 2>&1 &
  for _ in $(seq 1 50); do
    if running; then echo "started on http://$HOST:$PORT (pid $(cat "$PIDFILE"))"; return 0; fi
    sleep 0.2
  done
  echo "failed to start; see $LOGFILE"; tail -10 "$LOGFILE"; return 1
}
stop() {
  if running; then
    local pid
    pid="$(cat "$PIDFILE")"
    kill "$pid" 2>/dev/null
    for _ in $(seq 1 80); do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.25
    done
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null
      echo "forced stop"
    else
      echo "stopped"
    fi
  else
    echo "not running"
  fi
  rm -f "$PIDFILE"
}
backup() {
  mkdir -p "$BACKUP_DIR"
  local dest="$BACKUP_DIR/runchero-community-$(date +%Y%m%d-%H%M%S).db"
  "$PY" - "$DB" "$dest" <<'PY'
import sqlite3, sys
src, dest = sys.argv[1], sys.argv[2]
with sqlite3.connect(src) as source, sqlite3.connect(dest) as target:
    source.backup(target)
print(dest)
PY
}
case "${1:-status}" in
  start) start ;;
  stop) stop ;;
  restart) stop; start ;;
  status)
    if running; then echo "running (pid $(cat "$PIDFILE")) on http://$HOST:$PORT"; else echo "not running"; fi
    ;;
  backup) backup ;;
  *) echo "usage: $0 {start|stop|restart|status|backup}"; exit 2 ;;
esac
