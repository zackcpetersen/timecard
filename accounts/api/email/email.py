from django.core.mail import send_mail
from django.conf import settings


class EmailService:
    def __init__(self):
        self.default_from_email = settings.EMAIL_DEFAULT_FROM_ADDRESS

    def send_email(self, to_addr, subject, content):
        return send_mail(
            subject=subject,
            message=content,
            from_email=self.default_from_email,
            recipient_list=[to_addr],
        )
