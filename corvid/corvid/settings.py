"""
Django settings for corvid project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# make sure SECRET_KEY, DB_PASSWORD are defined in credentials.py
from corvid.credentials import SECRET_KEY
from corvid.credentials import DB_PASSWORD
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

'''
SECRET_KEY imported from a credentials module in this folder.
On a new machine, use the following snippet to generate a new key:

    python -c 'import django.utils.crypto as c; print(c.get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))' >> credentials.py
'''

# SECURITY WARNING: don't run with debug turned on in production!
if 'CORVID_PRODUCTION' in os.environ:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['corvid.xyz']

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = (
    'pagedown',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_forms_bootstrap',
    'main',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'corvid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'corvid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'corvid',
        'USER': 'corvid',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Security: we already force HTTPS on every single request via Nginx.  However,
# these are recommended in the Django deployment settings and certainly don't
# hurt anything.
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT = '/srv/www/static'
