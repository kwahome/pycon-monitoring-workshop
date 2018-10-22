FROM firehol/netdata:latest

MAINTAINER Urandu Bildad

COPY ./devops/netdata/master_stream.conf /etc/netdata/stream.conf
