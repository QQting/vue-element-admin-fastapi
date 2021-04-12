# This dockerfile aims to build the RMT-FastAPI development environment on Ubuntu 20.04
FROM ubuntu:focal
MAINTAINER Ting Chang <ting.chang@adlinktech.com>

# Install the necessary tools
RUN apt -qq update
RUN apt -qqy install git vim build-essential python3 python-is-python3 python3-distutils python3-pip curl

# Install poetry and configure env
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Download source codes
RUN cd /root && \
    git clone https://github.com/QQting/rmt-fastapi.git

# Install dependent python packages
RUN cd /root/rmt-fastapi/app && \
    poetry install -q

WORKDIR /root/rmt-fastapi/app/app
ENV LD_LIBRARY_PATH=/root/rmt-fastapi/app/app/api/api_v1/robots/RMT_core
