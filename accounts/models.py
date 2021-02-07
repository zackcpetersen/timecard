from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password,
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
        user.set_password(password)
        user.save()
        return user

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
