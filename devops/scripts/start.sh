#!/usr/bin/env bash

env=development
environment=$(env)

export FLASK_APP=app
export FLASK_ENV=${environment}

MIGRATIONS_DIR=migrations
LOG_TAG="INFO  [start.sh]"

if [ -d "$MIGRATIONS_DIR" ]; then
    echo "$LOG_TAG migrations already initiliazed..."
else
    echo "$LOG_TAG initializing migrations..."
    python manage.py db init
fi
echo "$LOG_TAG generating migrations file..."
python manage.py db migrate
echo "$LOG_TAG applying migrations..."
python manage.py db upgrade

python manage.py run
