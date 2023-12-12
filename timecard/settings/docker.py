import ast

from django.core.exceptions import ImproperlyConfigured

from timecard.settings.base import *


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


"""
Any settings that are wrapped in ast.literal_eval() should be set as boolean values.
They are returned as strings from the env, and anything other than an 
empty string will result in True, including 'False'

Any env variable with a `.split(" ")` should be a single string of hosts with a space between each.
For example: 'CORS_ORIGIN_WHITELIST=localhost 127.0.0.1'
"""

# Django settings
DEBUG = ast.literal_eval(get_env_variable('DEBUG'))
SECRET_KEY = get_env_variable('SECRET_KEY')
CORS_ALLOW_ALL_ORIGINS = ast.literal_eval(get_env_variable('CORS_ALLOW_ALL_ORIGINS'))
CORS_ALLOWED_ORIGIN_REGEXES.append(get_env_variable('CORS_ALLOWED_ORIGIN_REGEXES'))
ALLOWED_HOSTS.append(get_env_variable('ALLOWED_HOSTS'))
SECURE_SSL_REDIRECT = ast.literal_eval(get_env_variable('SECURE_SSL_REDIRECT'))
DEFAULT_DOMAIN = get_env_variable('DEFAULT_DOMAIN')
FRONTEND_URL = get_env_variable('FRONTEND_URL')

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT')
    }
}

# AWS settings
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings

USE_S3 = ast.literal_eval(get_env_variable('USE_S3'))
if USE_S3:
    STATIC_LOCATION = '/static/'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = get_env_variable('STATICFILES_STORAGE')
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = '/media/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = get_env_variable('DEFAULT_FILE_STORAGE')

# TODO maybe update to use emails this way?
# Email Settings
# EMAIL_HOST = get_env_variable('EMAIL_HOST')
# EMAIL_PORT = get_env_variable('EMAIL_PORT')
# EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
# EMAIL_USE_TLS = ast.literal_eval(get_env_variable('EMAIL_USE_TLS'))
# DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')
# EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')

# Gmail Settings
# Gmail Credentials - Emails will not send without these variables
GMAIL_CLIENT_ID = get_env_variable('GMAIL_CLIENT_ID')
GMAIL_PROJECT_ID = get_env_variable('GMAIL_PROJECT_ID')
GMAIL_CLIENT_SECRET = get_env_variable('GMAIL_CLIENT_SECRET')

