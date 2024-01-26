import secrets
import string

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import ImageOps, Image

from accounts.api.email.email import EmailService
from accounts import constants as account_constants


@receiver(models.signals.pre_save, sender='accounts.User')
def fix_image_orientation(sender, instance, **kwargs):
    if instance.image:
        old_obj = instance.__class__.objects.get(pk=instance.pk)
        if (not old_obj.image and instance.image) or (old_obj.image and old_obj.image != instance.image):
            with Image.open(instance.image) as image:
                image = ImageOps.exif_transpose(image)
                image.save(instance.image)


models.signals.pre_save.connect(fix_image_orientation, sender='accounts.User')


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
        email = EmailService()
        content = self.create_email_pass_content(user, rand_pass)
        email.send_email(user.email, subject, content)

    @staticmethod
    def create_email_pass_content(user, password):
        return account_constants.ACCOUNT_CREATION_MESSAGE.format(
            settings.FRONTEND_URL, user.first_name, user.last_name, user.email, password)

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

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
