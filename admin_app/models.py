from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add your other fields here

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('User groups'),
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('User permissions'),
        blank=True,
    )


# admin_app/models.py

from django.db import models


class User(models.Model):
    # Your user model fields go here
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


# models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


