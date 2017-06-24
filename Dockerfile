FROM python:3.6.1-alpine

LABEL maintainer jsanweb@gmail.com,sjbitcode.com
ENV PYTHONUNBUFFERED="TRUE" APP_PATH="/usr/src"

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

COPY ./requirements.txt .

# Install system dependencies and python packages.
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

ADD . $APP_PATH
