#!/usr/bin/env python2
"""
Fabric script to automate deployment!
"""

from fabric.api import *

USER = 'django'
REPO = '/home/django/corvid'
VENV = '/home/django/venv/bin/activate'


def deploy():
    sudo('service uwsgi stop corvid')
    sudo('service nginx stop')
    with cd(REPO):
        sudo('git pull', user=USER)
        sudo('source %s && python corvid/manage.py collectstatic' % VENV,
             user=USER)
        sudo('source %s && python corvid/manage.py makemigrations' % VENV,
             user=USER)
        sudo('source %s && python corvid/manage.py migrate' % VENV,
             user=USER)
    sudo('service uwsgi start corvid')
    sudo('service nginx start')
