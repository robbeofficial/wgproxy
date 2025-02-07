FROM alpine:latest

# Install necessary packages
RUN apk update && apk add --no-cache \
    wireguard-tools \
    iptables \
    tinyproxy \
    python3 \
    py3-pip \
    curl \
    bash \
    gettext \
    && rm -rf /var/cache/apk/*

# Copy code
COPY *.py .env /

# Install FastAPI and Uvicorn
RUN python3 -m venv /venv
RUN /venv/bin/pip install fastapi uvicorn requests python-dotenv

# Fetch wirguard configs
RUN /venv/bin/python3 fetch_wg_configs.py

# Copy configuration files
COPY tinyproxy /etc/tinyproxy/
COPY wireguard /etc/wireguard/

# Start script
CMD ["sh", "-c", "tinyproxy & /venv/bin/python3 /api.py"]
