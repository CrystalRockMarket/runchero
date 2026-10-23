#!/usr/bin/env bash
# Start, stop or restart the depot for local testing.
#
#   ./tools/depot.sh start [--port 8080]
#   ./tools/depot.sh stop
#   ./tools/depot.sh restart
#   ./tools/depot.sh status
#
# The pid is written to /tmp/runchero-depo.pid so stopping never has to hunt
# for the process by name.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE="/tmp/runchero-depo.pid"
LOGFILE="/tmp/runchero-depo.log"
HOST="${RID_HOST:-0.0.0.0}"
PORT="${RID_PORT:-8080}"

running() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null
}

start() {
  if running; then
    echo "already running (pid $(cat "$PIDFILE"))"
    return 0
  fi
  cd "$ROOT" || exit 1
  setsid nohup python3 run.py --host "$HOST" --port "$PORT" >"$LOGFILE" 2>&1 &
  echo $! >"$PIDFILE"
  sleep 1
  if running; then
    echo "started on http://$HOST:$PORT (pid $(cat "$PIDFILE"))"
  else
    echo "failed to start; see $LOGFILE"
    tail -5 "$LOGFILE"
    return 1
  fi
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
  *) echo "usage: $0 {start|stop|restart|status}"; exit 2 ;;
esac
