from fastapi import FastAPI
import subprocess
import random
import requests
import os
from pathlib import Path

app = FastAPI()

def get_wireguard_interface():
    # Run the wg show command
    result = subprocess.run(["wg", "show"], capture_output=True, text=True)

    # Process output and get the first interface name (if any)
    for line in result.stdout.splitlines():
        if line.startswith("interface:"):
            return line.split()[1]  # The second word is the interface name
    
    return None  # Return None if no WireGuard interface is active

def reconnect_wireguard(config):
    interface = get_wireguard_interface()
    if interface:
        subprocess.run(["wg-quick", "down", interface])    
    subprocess.run(["wg-quick", "up", config])

def get_public_ip():
    try:
        return requests.get('https://checkip.amazonaws.com').text.strip()
    except:
        return None
    
def get_configs():
    return [f.stem for f in Path('/etc/wireguard').glob('*.conf')]

@app.get("/renew_ip")
def renew_ip(config: str = None):
    if config is None:
        config = random.choice(get_configs())
    reconnect_wireguard(config)
    public_ip = get_public_ip()
    interface = get_wireguard_interface()
    return {"ip": public_ip, "interface": interface}

@app.get("/status")
def status():
    public_ip = get_public_ip()
    interface = get_wireguard_interface()
    return {"ip": public_ip, "interface": interface}

@app.get("/configs")
def configs():
    configs = get_configs()
    return {"configs": configs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
