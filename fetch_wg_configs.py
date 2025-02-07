import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

WIRESHARK_PRIVATE_KEY = os.getenv('WIRESHARK_PRIVATE_KEY')

# fetch wireshark configs (if WIRESHARK_PRIVATE_KEY is set)
if WIRESHARK_PRIVATE_KEY:
    print("Fetching Wireshark configs ...")
    target_dir = "/etc/wireguard/"

    clusters_endpoint = "https://api.surfshark.com/v4/server/clusters/generic"
    
    config_template = """[Interface]
    PrivateKey = {privKey}
    Address = 10.14.0.2/16
    DNS = 162.252.172.57, 149.154.159.92

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
            fp.write(config_template.format(**cluster, privKey=WIRESHARK_PRIVATE_KEY))