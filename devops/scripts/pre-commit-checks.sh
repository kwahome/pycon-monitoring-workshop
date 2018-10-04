#!/bin/bash

GITARGS=${1:-'diff --cached --name-only'}
git $GITARGS | grep -E '.py$' | xargs flake8 ''
[ $? -ne 0 ] && printf "\n\n\e[31m========= COMMIT REJECTED due to above listed style violations. ==========\e[0m\n\n" && exit 1
exit 0
