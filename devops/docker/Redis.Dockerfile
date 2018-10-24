FROM redis:3.2.10-alpine

MAINTAINER Urandu Bildad


RUN apk update
RUN apk -U upgrade
RUN apk add bash
RUN apk add autoconf automake bash build-base curl gawk git jq libuuid linux-headers musl-dev util-linux-dev libmnl-dev zlib-dev
RUN git clone https://github.com/netdata/netdata.git --depth=1 ~/netdata
RUN cd ~/netdata && ./netdata-installer.sh --dont-wait --dont-start-it

COPY ./devops/netdata/stream.conf /etc/netdata/stream.conf

RUN chmod 775 /etc/netdata/stream.conf

