from django_ses import SESBackend
from django.conf import settings


class CustomSESBackend(SESBackend):
    def __init__(self, *args, **kwargs):
        super(CustomSESBackend, self).__init__(
            *args, **kwargs,
            aws_access_key=settings.SES_ACCESS_KEY_ID,
            aws_secret_key=settings.SES_SECRET_ACCESS_KEY,
        )
