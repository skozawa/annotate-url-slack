from fabric.api import cd,run,sudo,put
import fabric.contrib.files
home_dir = '/var/www/apps/annotate-url-slack'
python = '/opt/python-3.6.1/bin/python3'


def setup():
    if not fabric.contrib.files.exists(home_dir):
        run("git clone git@github.com:skozawa/annotate-url-slack.git %s" % home_dir)
    pip_install()


def pip_install():
    with cd(home_dir):
        run('%s -m venv venv' % (python))
        run('. venv/bin/activate && pip install -q -r requirements.txt')


def update_config():
    with cd(home_dir):
        put('config/gspread-key.json', 'config/gspread-key.json')
        put('slackbot_settings.py', 'slackbot_settings.py')


def update():
    with cd(home_dir):
        run('git pull -q')
        run('git submodule update --init')
        pip_install()


def nginx(cmd):
    sudo('/usr/sbin/service nginx %s' % (cmd))


def supervisor(cmd, service='annotate'):
    if cmd in {'reload', 'reread'}:
        sudo('supervisorctl %s' % (cmd))
    else:
        sudo('supervisorctl %s %s' % (cmd, service))


def deploy():
    update()
    supervisor('restart')


def bot(cmd):
    supervisor(cmd, service='annotate-bot')
