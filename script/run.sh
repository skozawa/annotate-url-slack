#!/bin/sh
exec 2>&1
set -e

ROOT="/var/www/apps/annotate-url-slack"
CONFIG_FILE="$ROOT/config/gunicorn.conf.py"
PID=/var/run/gunicorn.pid

if [ -f $PID ]; then rm $PID; fi

export APP_ENV="production"
cd "$ROOT"
. $ROOT/venv/bin/activate
gunicorn -c $CONFIG_FILE annotate:app
