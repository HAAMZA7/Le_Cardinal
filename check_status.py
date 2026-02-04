
import paramiko
import sys

host = "82.165.198.165"
user = "root"
password = "Wv4cyNI3"

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=password)
    
    # Check status specifically for 'cardinal' service
    stdin, stdout, stderr = client.exec_command("systemctl status cardinal --no-pager")
    
    print("[*] Cardinal Service Status:")
    print(stdout.read().decode())
    
    # Also check sentinel.log tail to see what he is saying
    stdin, stdout, stderr = client.exec_command("tail -n 5 /root/Le_Cardinal/sentinel.log")
    print("\n[*] Sentinel Logs (Last 5 lines):")
    print(stdout.read().decode())

    client.close()

except Exception as e:
    print(f"[!] Error checking status: {e}")
