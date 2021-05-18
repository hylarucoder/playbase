FROM python:3.9.5-buster
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sed -i 's/deb.debian.org/mirrors.cloud.tencent.com/g' /etc/apt/sources.list
RUN sed -i 's/security.debian.org/mirrors.cloud.tencent.com/g' /etc/apt/sources.list
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y \
    vim \
    git \
    gcc \
    build-essential \
    libffi-dev \
    freetds-bin \
    krb5-user \
    ldap-utils \
    libffi6 \
    libsasl2-2 \
    libsasl2-modules \
    libssl1.1 \
    locales  \
    lsb-release \
    sasl2-bin \
    sqlite3 \
    unixodbc
ENV PYPI=https://mirrors.aliyun.com/pypi/simple/
ENV PIP_DEFAULT_TIMEOUT=1000
RUN pip install -U pip -i $PYPI
RUN pip install -U poetry -i $PYPI
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /opt/mipha
COPY . .
RUN poetry install
CMD ["start"]
