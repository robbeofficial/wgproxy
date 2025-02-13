import requests
import sys
import os

SURFSHARK_PRIVATE_KEY = os.getenv('SURFSHARK_PRIVATE_KEY')

# fetch surfshark configs (if SURFSHARK_PRIVATE_KEY is set)
if SURFSHARK_PRIVATE_KEY:
    print("Fetching Surfshark configs ...")
    target_dir = "/etc/wireguard/"

    clusters_endpoint = "https://api.surfshark.com/v4/server/clusters/generic"
    
    config_template = """[Interface]
PrivateKey = {privKey}
Address = 10.14.0.2/16
DNS = 162.252.172.57, 149.154.159.92
PostUp = ip route add $HOST_NETWORK via $DEFAULT_GATEWAY dev $DEFAULT_INTERFACE
PostDown = ip route del $HOST_NETWORK via $DEFAULT_GATEWAY dev $DEFAULT_INTERFACE

[Peer]
PublicKey = {pubKey}
AllowedIPs = 0.0.0.0/0
Endpoint = {connectionName}:51820"""

    # fetch clusters
    clusters = requests.get(clusters_endpoint).json()

    # write wireguard configs
    for cluster in clusters:
        fname = cluster["connectionName"].split('.')[0] + ".conf"
        with open(target_dir + "/" + fname, 'w') as fp:
            fp.write(config_template.format(**cluster, privKey=SURFSHARK_PRIVATE_KEY))