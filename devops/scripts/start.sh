#!/usr/bin/env bash

env=development
environment=$(env)

export FLASK_APP=app
export FLASK_ENV=${environment}

MIGRATIONS_DIR=migrations
INFO_LOG_TAG="INFO  [start.sh] "

logger(){
    echo "$INFO_LOG_TAG $1"
}

if [ -d "$MIGRATIONS_DIR" ]; then
    logger "migrations already initiliazed..."
else
    logger "initializing migrations..."
    python manage.py db init
fi
logger "generating migrations file..."
python manage.py db migrate
logger "applying migrations..."
python manage.py db upgrade
logger "starting flask app in environment='$environment'..."
logger " "
python manage.py run
