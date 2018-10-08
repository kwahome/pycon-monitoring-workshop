FROM swaggerapi/swagger-ui

MAINTAINER Kelvin Wahome

COPY ./devops/swagger-ui/swagger-ui-nginx.conf /etc/nginx/nginx.conf

ADD ./docs/api/swagger /usr/share/nginx/swagger/

COPY ./devops/scripts/swagger-ui-entrypoint.sh /usr/share/nginx/swagger-ui-entrypoint.sh

ENTRYPOINT ["/usr/share/nginx/swagger-ui-entrypoint.sh"]

CMD ["sh", "/usr/share/nginx/docker-run.sh"]
