FROM ubuntu:latest

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
        gcc \
        python3 \
        python3-dev \
        libsqlcipher-dev \
        ca-certificates \
        wget

RUN wget https://bootstrap.pypa.io/get-pip.py \
      && python3 get-pip.py

RUN pip3 install pyvault

ENTRYPOINT [ "vault" ]