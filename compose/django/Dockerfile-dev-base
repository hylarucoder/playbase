FROM ubuntu:16.04

MAINTAINER twocucao < twocucao@gmail.com >
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

COPY ./compose/django/sources.list /etc/apt/
RUN apt clean && apt update && apt upgrade -yq
RUN apt install -yq \
    build-essential \
    curl \
    git \
    ipython3 \
    libcurl4-openssl-dev \
    libffi-dev \
    libfreetype6-dev \
    libjpeg8-dev \
    liblcms2-dev \
    libgdal-dev \
    libpq-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libtiff5-dev \
    libwebp-dev \
    libxml2-dev \
    libxslt1-dev \
    libyaml-dev \
    locales \
    ntp \
    openssh-server \
    openssl \
    python3-lxml \
    python3-pip \
    python3-setuptools \
    python3-tk \
    python3.5-dev \
    python3.5 \
    sqlite3 \
    sudo \
    tcl8.6-dev \
    tk8.6-dev \
    vim \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Node JS

# gpg keys listed at https://github.com/nodejs/node
RUN set -ex \
  && for key in \
    9554F04D7259F04124DE6B476D5A82AC7E37093B \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    0034A06D9D9B0064CE8ADF6BF1747F4AD2306D93 \
    FD3A5288F042B6850C66B31F09FE44734EB7990E \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    B9AE9905FFD7803F25714661B63B535A4C206CA9 \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
  ; do \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
  done

ENV NODE_VERSION 8.9.3

RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --verify SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
    && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
    && rm "node-v$NODE_VERSION-linux-x64.tar.gz" SHASUMS256.txt.asc

