#!/usr/bin/env bash

INFO_LOG_TAG="INFO  [start.sh]"

echo "$INFO_LOG_TAG generating database migrations..."
python3 manage.py makemigrations core --settings=$DJANGO_SETTINGS_MODULE
echo "$INFO_LOG_TAG performing database migrations..."
python3 manage.py migrate --noinput --settings=$DJANGO_SETTINGS_MODULE
echo "$INFO_LOG_TAG collecting static files..."
python3 manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS_MODULE
echo "$INFO_LOG_TAG starting web server..."
# python3 manage.py runserver 0.0.0.0:80 --settings=$DJANGO_SETTINGS_MODULE
exec  gunicorn configuration.wsgi ${GUNICORN_BIND:- -b 0.0.0.0:80}\
         --workers=${GUNICORN_WORKERS:-8}\
         --log-level=DEBUG \
         --log-file=gunicorn.log\
         --access-logfile=access.log\
         --error-logfile=error.log\
         --timeout 100\
         --reload
