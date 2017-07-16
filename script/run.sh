#!/bin/sh
exec 2>&1
set -e

ROOT="/var/www/apps/annotate-url-slack"
cd "$ROOT"
CONFIG_FILE="$ROOT/config/gunicorn.conf.py"
export APP_ENV="production"

. $ROOT/venv/bin/activate && gunicorn -c $CONFIG_FILE annotate:app
