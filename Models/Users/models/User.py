from datetime import datetime
from typing import override

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):  # pyright: ignore[reportMissingTypeArgument]
    """Class to manage the creation of user objects"""
    
    def make_random_password(self, length=16):
        """Generates a random password of given length using allowed characters"""
        # define the allowed characters including all leters, digits, and some special characters
        allowed_chars = (
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789'
            '!@#$%^&*()-_=+[]{}|;:,.<>?'
        )
        # use random.choice to select characters from the allowed set and join them to form a password of the specified length
        import random
        return ''.join(random.choice(allowed_chars) for _ in range(length))
        
    def get_queryset(self):
        """Returns the queryset of users"""
        return super().get_queryset().filter(is_active=True)

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a user object
        Arguments:
        email: the string to use as email
        password: the string to use as password

        Optionals:
        Any additional fields to set on the User model

        Return:
            A user object
        """

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates an admin user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Return:
            A user object
        """
        user = self.create_user(email, password=password)
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name: models.CharField[str | None, str] = models.CharField(max_length=25, null=True, blank=True)
    last_name: models.CharField[str | None, str] = models.CharField(max_length=25, null=True, blank=True)
    username: models.CharField[str | None, str] = models.CharField(max_length=25, unique=True, null=True, blank=True)
    email: models.CharField[str | None, str] = models.EmailField(verbose_name='Email address', max_length=255, unique=True)
    is_active: models.BooleanField[bool, bool] = models.BooleanField(default=True)
    is_admin: models.BooleanField[bool, bool] = models.BooleanField(default=False)
    created_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(auto_now=True)


    USERNAME_FIELD: str = 'email'

    objects = UserManager()

    @override
    class Meta:
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"

    def __str__(self):
        return self.username or self.email

    def disable(self, *args, **kwargs):
        self.is_active ^= True
        self.save()

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    