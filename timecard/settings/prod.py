from .base import *  # noqa: F403

DEBUG = False

INTERNAL_IPS = []

if not os.environ.get("DJANGO_SECRET_KEY"):
    raise Exception("DJANGO_SECRET_KEY not set")
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# TODO update this to take from env vars
# # Get the environment variable
# items_str = os.getenv('MY_LIST', '')  # Provide a default empty string
#
# # Deserialize the string into a list
# items_list = items_str.split(',') if items_str else []
ALLOWED_HOSTS = ['backend.projecttimecard.com']
SECURE_SSL_REDIRECT = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Gmail Credentials - Emails will not send without these variables
if (not os.environ.get('GMAIL_CLIENT_ID')
        or not os.environ.get('GMAIL_PROJECT_ID')
        or not os.environ.get('GMAIL_CLIENT_SECRET')):
    raise Exception('Gmail Credentials not set')

GMAIL_CLIENT_ID = os.environ['GMAIL_CLIENT_ID']
GMAIL_PROJECT_ID = os.environ['GMAIL_PROJECT_ID']
GMAIL_AUTH_URI = "https://accounts.google.com/o/oauth2/auth" # nosec
GMAIL_TOKEN_URI = "https://oauth2.googleapis.com/token" # nosec
GMAIL_AUTH_PROVIDER = "https://www.googleapis.com/oauth2/v1/certs" # nosec
GMAIL_CLIENT_SECRET = os.environ['GMAIL_CLIENT_SECRET']
GMAIL_REDIRECT_URIS = ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]

# Live URL Settings
if 'FRONTEND_URL' in os.environ:
    FRONTEND_URL = os.environ['FRONTEND_URL']
else:
    FRONTEND_URL = 'https://www.projecttimecard.com'

# DB settings
if (not os.environ.get('RDS_DB_NAME')
        or not os.environ.get('RDS_USERNAME')
        or not os.environ.get('RDS_PASSWORD')
        or not os.environ.get('RDS_HOSTNAME')
        or not os.environ.get('RDS_PORT')):
    raise Exception('RDS Credentials not set')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://www.projecttimecard.com',
    'http://timecard-frontend-prod.s3-website-us-west-2.amazonaws.com'
]

if (not os.environ.get('AWS_ACCESS_KEY_ID')
        or not os.environ.get('AWS_SECRET_ACCESS_KEY')
        or not os.environ.get('AWS_STATIC_BUCKET')
        or not os.environ.get('AWS_S3_REGION_NAME')):
    raise Exception('AWS Credentials not set')

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STATIC_BUCKET = os.environ['AWS_STATIC_BUCKET']
AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
