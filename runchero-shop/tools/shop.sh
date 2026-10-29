#!/usr/bin/env bash
# Start, stop or restart the Runchero Beef shop for local testing.
#
#   ./tools/shop.sh start [--port 8081]
#   ./tools/shop.sh stop
#   ./tools/shop.sh restart
#   ./tools/shop.sh status
#   ./tools/shop.sh seed
#
# The pid is written to /home/barn/run/runchero-shop.pid so stopping never
# hunts for the process by name. The depot's pid file is never touched.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE="${RBS_PID_PATH:-/home/barn/run/runchero-shop.pid}"
LOGFILE="${RBS_LOG_PATH:-/home/barn/logs/runchero-shop.log}"
HOST="${RBS_HOST:-0.0.0.0}"
PORT="${RBS_PORT:-8081}"
PY="${PYTHON:-/usr/bin/python3}"

mkdir -p "$(dirname "$PIDFILE")" "$(dirname "$LOGFILE")"

running() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null
}

start() {
  if running; then
    echo "already running (pid $(cat "$PIDFILE"))"
    return 0
  fi
  cd "$ROOT" || exit 1
  rm -f "$PIDFILE"
  setsid nohup "$PY" run.py --host "$HOST" --port "$PORT" >>"$LOGFILE" 2>&1 &
  # The server writes its own pid once the port is bound, so wait for that
  # instead of trusting $! (setsid may or may not fork).
  for _ in $(seq 1 50); do
    if running; then
      echo "started on http://$HOST:$PORT (pid $(cat "$PIDFILE"))"
      return 0
    fi
    sleep 0.2
  done
  echo "failed to start; see $LOGFILE"
  tail -5 "$LOGFILE"
  return 1
}

stop() {
  if running; then
    kill "$(cat "$PIDFILE")" 2>/dev/null
    sleep 0.5
    echo "stopped"
  else
    echo "not running"
  fi
  rm -f "$PIDFILE"
}

seed() {
  cd "$ROOT" || exit 1
  "$PY" run.py --seed-only
}

case "${1:-status}" in
  start)   start ;;
  stop)    stop ;;
  restart) stop; start ;;
  status)
    if running; then
      echo "running (pid $(cat "$PIDFILE")) on http://$HOST:$PORT"
    else
      echo "not running"
    fi
    ;;
  seed)    seed ;;
  *) echo "usage: $0 {start|stop|restart|status|seed}"; exit 2 ;;
esac
