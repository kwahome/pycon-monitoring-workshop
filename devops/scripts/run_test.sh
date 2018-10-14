#!/usr/bin/env bash

docker-compose run web -e CC_TEST_REPORTER_ID=$CC_TEST_REPORTER_ID python manage.py test
