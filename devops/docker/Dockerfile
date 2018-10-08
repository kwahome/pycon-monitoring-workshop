FROM python:3

MAINTAINER Kelvin Wahome

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements/base.txt

EXPOSE 80

EXPOSE 443

CMD ./devops/scripts/start.sh
s