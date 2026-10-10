#!/bin/bash
set -e

echo "🚀 Cloud Browser Setup shuru ho raha hai..."

# System dependencies
echo "📦 System packages install ho rahe hain..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    xvfb \
    x11vnc \
    xfce4 \
    xfce4-terminal \
    novnc \
    websockify \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    > /dev/null 2>&1

# Python packages
echo "🐍 Python packages install ho rahe hain..."
pip install --quiet playwright asyncio fastapi uvicorn

# Playwright browsers install
echo "🌐 Playwright browser install ho raha hai..."
playwright install chromium
playwright install-deps chromium > /dev/null 2>&1

# Browser data folder (persistent logins yahan save honge)
mkdir -p /workspaces/cloud-browser/browser-data
mkdir -p /workspaces/cloud-browser/screenshots

# VNC password set karo (optional)
mkdir -p ~/.vnc
x11vnc -storepasswd "browser123" ~/.vnc/passwd 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo "▶️  Browser start karne ke liye: bash browser/start.sh"
echo "🔗 Browser dekhne ke liye: Port 6080 open karo (noVNC)"
