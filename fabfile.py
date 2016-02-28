#!/usr/bin/env python2
"""
Fabric script to automate deployment!
"""

from fabric.api import *

USER = 'django'
REPO = '/home/django/fugl'
VENV = '/home/django/venv/bin/activate'


def deploy():
    sudo('service uwsgi stop fugl')
    sudo('service nginx stop')
    with cd(REPO):
        sudo('git pull', user=USER)
        sudo('source %s && python fugl/manage.py collectstatic --noinput'
             % VENV, user=USER)
        sudo('source %s && python fugl/manage.py makemigrations' % VENV,
             user=USER)
        sudo('source %s && python fugl/manage.py migrate' % VENV,
             user=USER)
    sudo('service uwsgi start fugl')
    sudo('service nginx start')
