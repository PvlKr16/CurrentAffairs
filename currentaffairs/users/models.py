from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Email as login field
    email = models.EmailField(unique=True)

    # Additional fields
    is_guest = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Theme preference
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
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
