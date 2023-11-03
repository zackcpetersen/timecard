from .base import *  # noqa: F403

DEBUG = True

INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = ['*']
SECURE_SSL_REDIRECT = False
CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS += []

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_DIRS = []
