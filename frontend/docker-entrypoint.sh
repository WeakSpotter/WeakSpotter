#!/bin/sh

echo "window.__APP_CONFIG__ = { API_URL: "$API_URL" };" > /usr/share/nginx/html/config.js

nginx -g "daemon off;"
