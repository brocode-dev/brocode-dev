"""
Database User.
"""
import jwt

# from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manage for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_varified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the System."""
    email = models.EmailField(db_index=True,max_length=255, unique=True)
    username = models.CharField(max_length=255)
    # otp = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    # @property
    # def token(self):
    #     return self._generate_jwt_token()
    
    # def _generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(days=60)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token

class Otp(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_expire = models.BooleanField(default=False)
