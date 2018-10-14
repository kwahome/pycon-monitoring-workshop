#!/usr/bin/env bash

python /usr/local/bin/ansible-playbook devops/ansible/deploy.yml \
   --connection local -e "ENVIRONMENT=${ENVIRONMENT}" \
   -e "BROKER_URL=${BROKER_URL}"

set -e
rm -f celerybeat.pid
supervisord -c ./devops/supervisord/supervisord.conf
