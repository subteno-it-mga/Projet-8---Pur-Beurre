from . import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

sentry_sdk.init(
    dsn="https://28e2cc32cd6c481287d05a556a1c743a@o359264.ingest.sentry.io/5315920",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


SECRET_KEY = '%%180rD1fu|Soz_Ia|8p\x0b2;s'
DEBUG = False
ALLOWED_HOSTS = ['http://161.35.153.11/']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'purbeurre', # le nom de notre base de données créée précédemment
        'USER': 'martingaucher', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'felati61',
        'HOST': '',
        'PORT': '5432',
    }
}
