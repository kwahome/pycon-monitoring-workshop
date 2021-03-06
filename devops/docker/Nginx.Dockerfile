FROM nginx

MAINTAINER Kelvin Wahome

COPY ./devops/nginx/nginx.conf /etc/nginx/nginx.conf


RUN apt-get update
RUN apt-get install -y zlib1g-dev uuid-dev libmnl-dev gcc make autoconf autoconf-archive autogen automake pkg-config curl
RUN apt-get install -y python python-yaml python-mysqldb python-psycopg2 nodejs lm-sensors netcat git
RUN git clone https://github.com/netdata/netdata.git --depth=1 ~/netdata
RUN cd ~/netdata && ./netdata-installer.sh --dont-wait --dont-start-it

COPY ./devops/netdata/stream.conf /etc/netdata/stream.conf
COPY ./devops/netdata/web_log.conf /etc/netdata/python.d/web_log.conf

RUN chmod 775 /etc/netdata/stream.conf
RUN chmod 775 /etc/netdata/python.d/web_log.conf




RUN gpasswd -a nginx root
