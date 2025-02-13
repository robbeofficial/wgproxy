FROM alpine:latest

COPY *.py *.sh /
COPY tinyproxy /etc/tinyproxy/
COPY wireguard /etc/wireguard/

RUN chmod +x /entrypoint.sh

# Install system dependencies
RUN apk update && apk add --no-cache \
    wireguard-tools \
    iptables \
    gettext \
    tinyproxy \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/*

# Install python dependencies in a virtual environment
RUN python3 -m venv /venv \ 
    && /venv/bin/pip install fastapi uvicorn requests python-dotenv
    

# Fetch VPN configs using secrets mounts
RUN --mount=type=secret,id=SURFSHARK_PRIVATE_KEY,env=SURFSHARK_PRIVATE_KEY \
    /venv/bin/python3 fetch_wg_configs.py

CMD ["sh", "-c", "/entrypoint.sh"]
