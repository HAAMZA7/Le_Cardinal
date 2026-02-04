
# Le Cardinal - VPS Deployment Config

## Systemd Service
Create `/etc/systemd/system/cardinal.service`:

```ini
[Unit]
Description=Le Cardinal Sentinel
After=network.target

[Service]
User=root
WorkingDirectory=/root/Le_Cardinal
ExecStart=/usr/bin/python3 sentinel.py
Restart=always
Environment="TELEGRAM_TOKEN=YOUR_TOKEN"
Environment="TELEGRAM_CHAT_ID=YOUR_ID"

[Install]
WantedBy=multi-user.target
```

## Setup Commands
```bash
cd /root
git clone https://github.com/HAAMZA7/Le_Cardinal.git
cd Le_Cardinal
pip3 install requests psutil
cp cardinal.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable cardinal
systemctl start cardinal
```
