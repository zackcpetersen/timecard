import secrets
import string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from accounts.api.gmail.gmail_service import GmailAPI
from accounts import constants as account_constants


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None,
                    is_admin=False, is_superuser=False):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = is_admin
        if is_superuser:
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
        if password:
            user.pass_valid = True
            user.set_password(password)
            user.save()
            return user
        email_subj = account_constants.CREATION_SUBJECT.format(user.first_name, user.last_name)
        self.email_random_pass(user, email_subj)
        return user

    @staticmethod
    def create_random_pass(length=10):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def email_random_pass(self, user, subject):
        rand_pass = self.create_random_pass()
        user.set_password(rand_pass)
        user.pass_valid = False
        user.save()
        # TODO credentials.json will need to be setup with new gmail account
        #  - https://developers.google.com/gmail/api/quickstart/python - Enable the Gmail API button
        email = GmailAPI(user, rand_pass, subject)
        email.send_pass_details()

    def create_superuser(self, email, first_name, last_name, password):
        user = User(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='Email Address', max_length=255,
                              unique=True, db_index=True, )
    image = models.ImageField(upload_to='profile-images',
                              null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    pass_valid = models.BooleanField(default=True)
