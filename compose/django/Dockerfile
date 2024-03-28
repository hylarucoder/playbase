FROM python:3.11.8-bullseye
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y \
		liblzma-dev \
    build-essential \
    cmake \
    curl \
    freetds-bin \
    gcc \
    git \
    krb5-user \
    ldap-utils \
    libbz2-dev \
    libffi-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsasl2-2 \
    libsasl2-modules \
    libsqlite3-dev \
    libssl-dev \
    libssl1.1 \
    llvm \
    locales  \
    lsb-release \
    sasl2-bin \
    sqlite3 \
    unixodbc \
    vim \
    wget \
    xz-utils \
    zlib1g-dev \
    tk-dev

ENV PYPI=https://mirrors.cloud.tencent.com/pypi/simple
ENV PIP_DEFAULT_TIMEOUT=1000
RUN pip install -U pip -i $PYPI
RUN pip install -U poetry -i $PYPI
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /opt/playbase
COPY . .
RUN poetry install
CMD ["start"]
