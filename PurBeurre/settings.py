"""
Django settings for PurBeurre project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_FILE = os.path.join(BASE_DIR, 'secret.txt')

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:  # pragma : no-cover
    try:
        import random
        SECRET_KEY = ''.join([random.SystemRandom().choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
            for i in range(50)])
        secret = open(SECRET_FILE, 'w')
        secret.write(SECRET_KEY)
        secret.close()
    except IOError:  # pragma : no-cover
        Exception('Please create a %s file with random characters \
        to generate your secret key!' % SECRET_FILE)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ON_HEROKU = os.environ.get('ON_HEROKU')
ON_PROD = 'PRODUCTION' in os.environ

if ON_PROD or ON_HEROKU:  # pragma : no-cover
    DEBUG = False
else:
    DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'search_food.apps.SearchFoodConfig',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'PurBeurre.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'standard/templates')
        ],
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

WSGI_APPLICATION = 'PurBeurre.wsgi.application'

if ON_HEROKU:  # pragma : no-cover
    DATABASES = {'default': dj_database_url.config()}
    ALLOWED_HOSTS = ['herokupurbeurremga.herokuapp.com']
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'purbeurre',
            'USER': 'martingaucher',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '5432',
        }
    }
    ALLOWED_HOSTS = ['*']


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()

if ON_PROD or ON_HEROKU:  # pragma : no-cover
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

import django_heroku
django_heroku.settings(locals())