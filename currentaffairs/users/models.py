from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)

    is_guest = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    LANGUAGE_CHOICES = [
        ('be', 'Беларуская'),
        ('en', 'English'),
        ('it', 'Italiano'),
        ('lt', 'Lietuvių'),
        ('ru', 'Русский'),
        ('ua', 'Українська'),
    ]

    native_language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    COLOR_CHOICES = [
        ('emerald', 'Emerald'),
        ('ultramarine', 'Ultramarine'),
        ('violet_orange', 'Violet & Orange'),
    ]

    color_scheme = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='emerald'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Auto-fill username from email
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
