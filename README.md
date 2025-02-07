# wgproxy
Proxy server behind WireGuard connection with simple REST API

# Usage
1. Add your custom wireguard configs to the `wireguard` folder or add the API Key of your VPN provider to the `.env` file. Currently, only Wireshark VPN is supported.
1. Build the docker image using `$ just build`. This step will copy your wireguard configs into the image and fetch the configs from your VPN provider direclty, if key is provided. 
1. Run container using `$ just run`. 
1. Route traffic through the proxy server, e.g. using `$ curl --proxy localhost:8888 api.ipify.org`.
1. Control the proxy server using the provided REST API, e.g. using `$ curl localhost:8000/renew_ip`