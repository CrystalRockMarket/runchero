#!/usr/bin/env bash
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE="${RLK_PID_PATH:-/home/barn/run/runchero-links.pid}"
LOGFILE="${RLK_LOG_PATH:-/home/barn/logs/runchero-links.log}"
HOST="${RLK_HOST:-0.0.0.0}"
PORT="${RLK_PORT:-8091}"
PY="${PYTHON:-/usr/bin/python3}"
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
case "${1:-status}" in
  start) start ;;
  stop) stop ;;
  restart) stop; start ;;
  status)
    if running; then echo "running (pid $(cat "$PIDFILE")) on http://$HOST:$PORT"; else echo "not running"; fi
    ;;
  *) echo "usage: $0 {start|stop|restart|status}"; exit 2 ;;
esac
