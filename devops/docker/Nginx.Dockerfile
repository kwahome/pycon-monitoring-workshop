FROM nginx

MAINTAINER Kelvin Wahome

COPY ./devops/nginx/nginx.conf /etc/nginx/nginx.conf

RUN gpasswd -a nginx root
