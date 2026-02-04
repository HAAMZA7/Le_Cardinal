#!/bin/bash
# Install script for Le Cardinal on VPS

echo "[*] Installing Python dependencies..."
apt-get update && apt-get install -y python3-pip
pip3 install requests psutil --break-system-packages

echo "[*] Setting up Environment..."
# Inject tokens from existing ChouetteVeille env if possible, or use placeholders
# We will create a simple .env loader wrapper for the service
# For now, let's hardcode the keys into the service file purely for this "solo dev" context deployment
# Retrieving keys from the environment where this script runs? No, we are on the VPS.
# We will trust the user to have set them or we inject them now.

echo "[*] Configuring Systemd Service..."
if [ -f "cardinal.service" ]; then
    cp cardinal.service /etc/systemd/system/
    
    # Reload and Start
    systemctl daemon-reload
    systemctl enable cardinal
    systemctl restart cardinal
    
    echo "[+] Le Cardinal Service Started!"
    systemctl status cardinal --no-pager
else
    echo "[!] Error: cardinal.service not found!"
    exit 1
fi
