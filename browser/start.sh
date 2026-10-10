#!/bin/bash

echo "🖥️  Virtual Display start ho raha hai..."
# Kill any existing Xvfb
pkill Xvfb 2>/dev/null || true
pkill x11vnc 2>/dev/null || true
pkill websockify 2>/dev/null || true
sleep 1

# Start virtual display (1280x720 resolution)
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99
sleep 2

# Start XFCE desktop (lightweight)
startxfce4 &
sleep 3

echo "🔒 VNC Server start ho raha hai..."
x11vnc -display :99 -nopw -listen localhost -xkb -forever -shared -quiet &
sleep 2

echo "🌐 noVNC start ho raha hai (port 6080)..."
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &
sleep 1

echo ""
echo "✅ Browser environment ready!"
echo "👁️  Dekhne ke liye: Ports tab mein 6080 open karo"
echo "🎮 Control karne ke liye: python browser/controller.py"
echo ""
echo "🌍 Ab Chromium start ho raha hai..."

# Chromium start with persistent data and remote debugging
chromium-browser \
    --display=:99 \
    --user-data-dir=/workspaces/cloud-browser/browser-data \
    --remote-debugging-port=9222 \
    --no-first-run \
    --no-default-browser-check \
    --disable-infobars \
    --window-size=1280,720 \
    --start-maximized \
    2>/dev/null &

echo "✅ Chromium chal raha hai! noVNC mein dekho."

# Keep running
wait
