# wgproxy
Dockerized proxy server behind WireGuard connection with simple REST API

wgproxy provides endpoints to manage and interact with WireGuard VPN configurations. It allows you to renew your IP address by switching between different WireGuard configurations, check the current status of your VPN connection, and list available configurations.

# Usage
1. Add your custom wireguard configs to the `wireguard` folder, or add the API Key of your VPN provider to the `.env` file.
1. Build the docker image using `$ just build`. This step will fetch wireguard configs from your VPN provided when the API key is set. Currently, only Surfshark VPN is supported for autofetch. 
1. Run container using `$ just run`. 
1. Route traffic through the proxy server, e.g. using `$ curl --proxy localhost:8888 api.ipify.org`.
1. Control the proxy server using the provided REST API, e.g. using `$ curl localhost:8000/renew_ip`

# API Endpoints

## Renew IP

Renews the public IP address by reconnecting to a WireGuard configuration. If no specific configuration is provided, a random one is selected.

- **URL**: `/renew_ip`
- **Method**: `GET`
- **Query Parameters**:
  - `config` (optional): The name of the WireGuard configuration to use (without the `.conf` extension). If not provided, a random configuration is selected.
- **Response**:
  - `ip`: The new public IP address after reconnecting.
  - `interface`: The WireGuard interface currently in use.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/renew_ip?config=wg0"
```

**Example Response**:
```json
{
  "ip": "203.0.113.1",
  "interface": "wg0"
}
```

---

## Status

Returns the current public IP address and the active WireGuard interface.

- **URL**: `/status`
- **Method**: `GET`
- **Response**:
  - `ip`: The current public IP address.
  - `interface`: The WireGuard interface currently in use.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/status"
```

**Example Response**:
```json
{
  "ip": "203.0.113.1",
  "interface": "wg0"
}
```

---

## Configs

Lists all available WireGuard configurations in the `/etc/wireguard` directory.

- **URL**: `/configs`
- **Method**: `GET`
- **Response**:
  - `configs`: A list of available WireGuard configuration names (without the `.conf` extension).

**Example Request**:
```bash
curl -X GET "http://localhost:8000/configs"
```

**Example Response**:
```json
{
  "configs": ["wg0", "wg1", "wg2"]
}
```