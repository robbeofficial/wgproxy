set shell := ["bash", "-uc"]

build:
    docker build -t wgproxy .

shell:
    docker run --rm --privileged -it -p 8000:8000 -p 8888:8888 --env-file .env wgproxy /bin/bash

run:
    docker run --rm --privileged -p 8000:8000 -p 8888:8888 --env-file .env wgproxy