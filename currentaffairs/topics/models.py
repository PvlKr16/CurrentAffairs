from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    is_open = models.BooleanField(default=True)

    participants = models.ManyToManyField(
        User,
        related_name='topics',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TopicReadStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    last_read_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user} - {self.topic}"
