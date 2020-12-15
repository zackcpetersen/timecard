import os

from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="zack@gmail.com").exists():
            password = os.environ.get('SUPERUSER_AUTH_PASS') if os.environ.get('SUPERUSER_AUTH_PASS') else 'admin'
            User.objects.create_superuser(email="zack@gmail.com",
                                          password=password,
                                          first_name='Zack',
                                          last_name='Petersen')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
