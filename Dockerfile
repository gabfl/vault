FROM ubuntu:latest

RUN export DEBIAN_FRONTEND=noninteractive \
      && apt-get update \
      && apt install tzdata \
      && ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime \
      && dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -y --no-install-recommends \
        gcc \
        python3 \
        python3-dev \
        ca-certificates \
        wget \
        git \
        build-essential \
        tcl8.6-dev \
        libssl-dev

RUN git clone https://github.com/sqlcipher/sqlcipher.git \
      && cd sqlcipher \
      && ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC" LDFLAGS="-lcrypto" \
      && make \
      && make install \
      && apt install libsqlcipher0

RUN wget https://bootstrap.pypa.io/get-pip.py \
      && python3 get-pip.py

# RUN git clone -b pyperclip-except https://github.com/gabfl/vault.git \
#       && cd vault \
#       && pip3 install .

RUN pip3 install pyvault

ENTRYPOINT [ "/bin/bash", "-c", "sqlcipher --version && pip3 freeze | grep pyvault && vault" ]