#!/bin/sh
set -eu

if [ -f /tmp/.X99-lock ]; then
	old_pid=$(cat /tmp/.X99-lock 2>/dev/null || true)
	case "$old_pid" in
		''|*[!0-9]*) ;;
		*) kill "$old_pid" 2>/dev/null || true ;;
	esac
	rm -f /tmp/.X99-lock
fi
rm -f /tmp/.X11-unix/X99

Xvfb :99 -screen 0 1280x900x24 -ac &
until xdpyinfo -display :99 >/dev/null 2>&1; do
	sleep 1
done
fluxbox >/tmp/fluxbox.log 2>&1 &
x11vnc -display :99 -forever -shared -rfbport 5900 -nopw >/tmp/x11vnc.log 2>&1 &
websockify --web=/usr/share/novnc 6080 localhost:5900 >/tmp/websockify.log 2>&1 &

python main.py >/tmp/npl-analysis.log 2>&1 &
python -m flask --app app run --host=0.0.0.0 --port=5000 >/tmp/flask.log 2>&1 &
flask_pid=$!

sleep 2
chromium --no-sandbox --disable-dev-shm-usage http://127.0.0.1:5000 >/tmp/chromium.log 2>&1 &

wait "$flask_pid"