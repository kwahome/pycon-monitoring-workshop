FROM firehol/netdata:latest

MAINTAINER Urandu Bildad

COPY ./devops/netdata/master_stream.conf /etc/netdata/stream.conf
COPY ./devops/netdata/health_alarm_notify.conf /etc/netdata/health_alarm_notify.conf
