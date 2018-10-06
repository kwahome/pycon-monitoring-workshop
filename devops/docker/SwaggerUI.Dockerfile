FROM swaggerapi/swagger-ui

EXPOSE 8080

COPY ./docs/api/swagger /docs/api/swagger

ENV SWAGGER_JSON "/api/docs/send-message.yml"

CMD ["sh", "/usr/share/nginx/docker-run.sh"]