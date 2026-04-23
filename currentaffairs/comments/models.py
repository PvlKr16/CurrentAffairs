from django.db import models
from django.conf import settings
from topics.models import Topic

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    file = models.FileField(
        upload_to='comments/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.author} - {self.topic}"


class CommentAttachment(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='comments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
