
import os
import time
import requests
import psutil
from datetime import datetime

# Cardinal Sentinel - Heartbeat & Monitoring Script
# Runs on VPS to check health of itself and ChouetteVeille

LOG_FILE = "sentinel.log"
CHOUETTE_API = "http://localhost:5000/api/stats"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def send_alert(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        log("No Telegram Token, skipping alert: " + msg)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"🚨 [SENTINEL] {msg}"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        log(f"Failed to send alert: {e}")

def check_chouette():
    try:
        # Use Basic Auth if needed, but locally localhost might be open or we use env vars
        # For now simple check
        r = requests.get(CHOUETTE_API, timeout=5)
        if r.status_code == 200:
            return True, r.json()
        return False, f"Status {r.status_code}"
    except Exception as e:
        return False, str(e)

def check_system():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, mem, disk

def main():
    log("Sentinel Started.")
    fails = 0
    
    while True:
        # 1. System Health
        cpu, mem, disk = check_system()
        if cpu > 90 or mem > 90 or disk > 90:
            send_alert(f"High Load! CPU: {cpu}%, RAM: {mem}%, DISK: {disk}%")
        
        # 2. ChouetteVeille Health
        ok, data = check_chouette()
        if not ok:
            fails += 1
            log(f"ChouetteVeille Down! ({fails}/3) - {data}")
            if fails >= 3:
                send_alert(f"ChouetteVeille API is DOWN after 3 attempts. Error: {data}")
                # Optional: os.system("systemctl restart chouetteveille")
                fails = 0 # Reset to avoid spam
        else:
            fails = 0
            
        time.sleep(60) # Constant monitoring

if __name__ == "__main__":
    main()
