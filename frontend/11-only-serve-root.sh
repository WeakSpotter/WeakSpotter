#!/bin/sh

set -e

DEFAULT_CONF_FILE="etc/nginx/conf.d/default.conf"

entrypoint_log() {
    if [ -z "${NGINX_ENTRYPOINT_QUIET_LOGS:-}" ]; then
        echo "$@"
    fi
}

if [ ! -f "/$DEFAULT_CONF_FILE" ]; then
    entrypoint_log "$ME: info: /$DEFAULT_CONF_FILE is not a file or does not exist"
    exit 0
fi

# check if the file can be modified, e.g. not on a r/o filesystem
touch /$DEFAULT_CONF_FILE 2>/dev/null || { entrypoint_log "$ME: info: can not modify /$DEFAULT_CONF_FILE (read-only file system?)"; exit 0; }

sed -i '/location \/ {/,/}/c\    location / {\n        root   /usr/share/nginx/html;\n        index  index.html;\n        try_files $uri /index.html;\n    }' "/$DEFAULT_CONF_FILE"
