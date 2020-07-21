from . import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}