#! /bin/sh

echo "starting preparing swagger files"
set -e
NGX_ROOT="/usr/share/nginx"
SWAGGER_DIR="swagger"

INFO_LOG_TAG="INFO  [swagger-ui-entrypoint.sh]"

for file in "$NGX_ROOT/$SWAGGER_DIR"/*; do
    echo "$INFO_LOG_TAG file to sed: $file"
    # check if file is of type file
    if [[ -f $file ]]; then
        sed -e "s/<HOST>/$SWAGGER_HOST/" "$file" > "$NGX_ROOT/html/${file##*/}"
    fi
     if [ $? -eq 0 ]; then
        echo "$INFO_LOG_TAG [success] ${file##*/} swagger file sed succeeded"
    else
        echo "$INFO_LOG_TAG [error] ${file##*/} swagger file sed failed"
    fi
done
echo "$INFO_LOG_TAG done preparing swagger files"
exec "$@"
