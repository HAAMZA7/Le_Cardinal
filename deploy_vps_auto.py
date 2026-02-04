
import paramiko
import time
import sys

host = "82.165.198.165"
user = "root"
password = "Wv4cyNI3"

print(f"[*] Connecting to {host}...")

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=password)
    print(f"[+] Connected to {host} as {user}!")

    commands = [
        "cd /root",
        "rm -rf Le_Cardinal", # Clean start
        "git clone https://github.com/HAAMZA7/Le_Cardinal.git",
        "cd Le_Cardinal",
        "chmod +x scripts/install_vps.sh",
        "./scripts/install_vps.sh"
    ]

    full_cmd = " && ".join(commands)
    print(f"[*] Executing remote commands: {full_cmd}")

    stdin, stdout, stderr = client.exec_command(full_cmd)

    # Stream output
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line.strip())

    err = stderr.read().decode()
    if err:
        print("[!] Stderr Output:")
        print(err)

    client.close()
    print("[+] Deployment sequence completed.")

except Exception as e:
    print(f"[!] Critical Error: {e}")
    sys.exit(1)
