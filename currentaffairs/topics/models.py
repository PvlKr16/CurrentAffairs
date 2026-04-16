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

class Poll(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.TextField()
    file = models.FileField(
        upload_to='polls/',
        blank=True,
        null=True
    )

    is_open = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    allow_multiple = models.BooleanField(default=False)

    participants = models.ManyToManyField(
        User,
        related_name='polls',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]


class PollOption(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='options'
    )

    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class PollVote(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    option = models.ForeignKey(
        PollOption,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'option', 'user')
