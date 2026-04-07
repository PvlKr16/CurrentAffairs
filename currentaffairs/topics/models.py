from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    is_open = models.BooleanField(default=True)

    participants = models.ManyToManyField(User, related_name='topics')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
