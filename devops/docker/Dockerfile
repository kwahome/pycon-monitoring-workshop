FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements/base.txt

EXPOSE 5000

CMD ./devops/scripts/start.sh