set dotenv-load
set shell := ["bash", "-uc"]

build:
    docker build --secret id=SURFSHARK_PRIVATE_KEY -t wgproxy .

shell:
    docker run --rm --privileged --env-file .env -it -p 8000:8000 -p 8888:8888 wgproxy sh

run:
    docker run --rm --privileged --env-file .env -p 8000:8000 -p 8888:8888 wgproxy