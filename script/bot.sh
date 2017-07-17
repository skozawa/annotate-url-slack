#!/bin/sh
exec 2>&1
set -e

ROOT="/var/www/apps/annotate-url-slack"

export APP_ENV="production"
cd "$ROOT"
. venv/bin/activate
python script/bot.py
