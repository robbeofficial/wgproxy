FROM alpine:latest

COPY *.py .env /
COPY tinyproxy /etc/tinyproxy/
COPY wireguard /etc/wireguard/

RUN apk update && apk add --no-cache \
    wireguard-tools \
    iptables \
    tinyproxy \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/* \
    && python3 -m venv /venv \ 
    && /venv/bin/pip install fastapi uvicorn requests python-dotenv \
    && export $(grep -v '^#' .env | xargs) \
    && /venv/bin/python3 fetch_wg_configs.py

CMD ["sh", "-c", "tinyproxy & /venv/bin/python3 /api.py"]
