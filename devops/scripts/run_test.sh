#!/usr/bin/env bash

set -e

pip install black && ./devops/scripts/pre-commit-checks.sh "diff-tree --no-commit-id --name-only -r HEAD"
coverage erase
./devops/scripts/wait-for-it.sh db:5432
coverage run --omit="*virtualenvs/*,*settings*,*manage*,*migrations*,*__init__*,*admin*,*celery*,*docs/*," manage.py test && bash <(curl -s https://codecov.io/bash)
coverage report --show-missing
