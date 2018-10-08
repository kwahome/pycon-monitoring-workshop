#!/usr/bin/env bash

INFO_LOG_TAG="INFO  [start.sh]"

echo "$INFO_LOG_TAG performing database migrations..."
python3 manage.py migrate --noinput --settings=$DJANGO_SETTINGS_MODULE
echo "$INFO_LOG_TAG collecting static files..."
python3 manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS_MODULE
echo "$INFO_LOG_TAG starting web server..."
python3 manage.py runserver 0.0.0.0:80 --settings=$DJANGO_SETTINGS_MODULE
