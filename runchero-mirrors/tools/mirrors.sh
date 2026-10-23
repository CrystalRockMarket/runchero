#!/usr/bin/env bash
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE="${RMM_PID_PATH:-/home/barn/run/runchero-mirrors.pid}"
LOGFILE="${RMM_LOG_PATH:-/home/barn/logs/runchero-mirrors.log}"
HOST="${RMM_HOST:-0.0.0.0}"
PORT="${RMM_PORT:-8090}"
mkdir -p "$(dirname "$PIDFILE")" "$(dirname "$LOGFILE")" /home/barn/mirrors /home/barn/data
running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }
start() {
  if running; then echo "already running (pid $(cat "$PIDFILE"))"; return 0; fi
  cd "$ROOT" || exit 1
  rm -f "$PIDFILE"
  setsid nohup python3 run.py --host "$HOST" --port "$PORT" >>"$LOGFILE" 2>&1 &
  for _ in $(seq 1 50); do
    if running; then echo "started on http://$HOST:$PORT (pid $(cat "$PIDFILE"))"; return 0; fi
    sleep 0.2
  done
  echo "failed to start; see $LOGFILE"; tail -10 "$LOGFILE"; return 1
}
stop() { if running; then kill "$(cat "$PIDFILE")" 2>/dev/null; sleep 0.5; echo "stopped"; else echo "not running"; fi; rm -f "$PIDFILE"; }
seed() { cd "$ROOT" || exit 1; python3 run.py --seed-only; }
case "${1:-status}" in start) start ;; stop) stop ;; restart) stop; start ;; status) if running; then echo "running (pid $(cat "$PIDFILE")) on http://$HOST:$PORT"; else echo "not running"; fi ;; seed) seed ;; *) echo "usage: $0 {start|stop|restart|status|seed}"; exit 2 ;; esac
