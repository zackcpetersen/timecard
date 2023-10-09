from .base import *

DEBUG = False

INTERNAL_IPS = ['127.0.0.1']

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS.append('127.0.0.1')
SECURE_SSL_REDIRECT = False

LOGGING = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timecard',
        'USER': 'timecard',
        'PASSWORD': 'timecard',
        'HOST': 'localhost',
        'PORT': '5431',
    }
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_DIRS = []
