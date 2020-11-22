from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="zack@gmail.com").exists():
            User.objects.create_superuser(email="zack@gmail.com",
                                          password="admin",
                                          first_name='Zack',
                                          last_name='Petersen')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
