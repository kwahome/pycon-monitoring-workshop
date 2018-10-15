#!/usr/bin/env bash

set -e

# download codeclimate test coverage reporter program
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 >/usr/local/bin/cc-test-reporter &&
  chmod +x /usr/local/bin/cc-test-reporter

pip install black && ./devops/scripts/pre-commit-checks.sh "diff-tree --no-commit-id --name-only -r HEAD"
cc-test-reporter before-build
coverage erase
./devops/scripts/wait-for-it.sh db:5432
coverage run --omit="*virtualenvs/*,*settings*,*manage*,*migrations*,*__init__*,*admin*,*celery*,*docs/*," manage.py test ||
  exit 1
bash <(curl -s https://codecov.io/bash)

# if test coverage is less than 85%, the following command will exit with status code 2; thus failing the build
coverage report --fail-under=80 || COVERAGE_REPORT_FAILED="yes"
[[ $COVERAGE_REPORT_FAILED == "yes" ]] && printf '\n\n test code coverage is below required 80 percent. \n\n' && exit 2

coverage xml
cc-test-reporter after-build --exit-code $?
