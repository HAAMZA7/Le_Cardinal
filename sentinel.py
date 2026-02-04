
import os
import time
import requests
import psutil
import json
import subprocess
from datetime import datetime

# Cardinal Assistant - Interactive Telegram Bot
# Runs on VPS. Listens for commands via Long Polling.

LOG_FILE = "sentinel.log"
CHOUETTE_API = "http://localhost:5000/api/stats"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OFFSET = 0

AUTH = ('hamza', 'Vincero-77') # Hardcoded for reliability in this specific deployment

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def send_msg(text):
    if not TELEGRAM_TOKEN or not ALLOWED_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": ALLOWED_CHAT_ID, "text": text})
    except Exception as e:
        log(f"Send failed: {e}")

def get_updates():
    global OFFSET
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"offset": OFFSET, "timeout": 30}
    try:
        r = requests.get(url, params=params, timeout=40)
        if r.status_code == 200:
            data = r.json()
            if data['ok']:
                return data['result']
    except Exception as e:
        log(f"Polling error: {e}")
    return []

def handle_command(cmd):
    cmd = cmd.lower().strip()
    
    if cmd == "/start":
        return "👋 Bonjour Hamza. Le Cardinal est à l'écoute.\nCommandes: /status, /scan, /logs, /sys"
        
    if cmd == "/status":
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        try:
            r = requests.get(CHOUETTE_API, auth=AUTH, timeout=5)
            cv_status = "✅ ONLINE" if r.status_code == 200 else f"❌ ERROR {r.status_code}"
            cv_uptime = r.json().get('uptime_days', '?') if r.status_code == 200 else "?"
        except Exception as e:
            cv_status = f"❌ DOWN ({str(e)})"
            cv_uptime = "0"
            
        return f"📊 **Rapport Situation**\n\n🖥 **VPS**\nCPU: {cpu}%\nRAM: {mem}%\n\n🦉 **ChouetteVeille**\nEtat: {cv_status}\nUptime: {cv_uptime}j"

    if cmd == "/logs":
        try:
            # Get last 5 lines of ChouetteVeille log (assuming location)
            # Actually let's get sentinel log for now
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()[-5:]
            return "📜 **Derniers Logs Cardinal:**\n" + "".join(lines)
        except:
            return "Pas de logs disponibles."

    if cmd == "/sys":
        uptime = subprocess.getoutput("uptime -p")
        disk = subprocess.getoutput("df -h / | tail -1 | awk '{print $5}'")
        return f"⚙️ **System Info**\n{uptime}\nDisk Usage: {disk}"

    return "Commande inconnue. Essayez /status."

def main():
    global OFFSET
    log("Cardinal Assistant Started.")
    send_msg("🍷 Le Cardinal est en ligne (Mode Assistant).")
    
    while True:
        updates = get_updates()
        for u in updates:
            OFFSET = u['update_id'] + 1
            msg = u.get('message', {})
            chat_id = str(msg.get('chat', {}).get('id'))
            text = msg.get('text', '')
            
            # Security Check
            if chat_id != str(ALLOWED_CHAT_ID):
                log(f"Unauthorized access attempt from {chat_id}")
                continue
                
            if text.startswith("/"):
                log(f"Command received: {text}")
                response = handle_command(text)
                send_msg(response)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
