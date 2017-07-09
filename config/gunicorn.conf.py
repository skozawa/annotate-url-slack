# http://docs.gunicorn.org/en/stable/settings.html
# Server Socket
bind = ':8000'

# Worker Processes
workers = 5
timeout = 60

# Server Mechanics
chdir = '/var/www/annotate-url-slack'
raw_env = 'APP_ENV=production'
pidfile = '/var/run/gunicorn.pid'
user = 'www-data'
group = 'www-data'

# Logging
accesslog = '/var/log/app/annotate_access_log'
errorlog = '/var/log/app/annotate_error_log'
