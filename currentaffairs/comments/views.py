from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import CommentForm
from .models import Comment, CommentAttachment
from topics.models import Topic, TopicReadStatus


@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    form = CommentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.topic = topic

            # ❗ отключаем старое поле
            comment.file = None

            comment.save()

            # ✅ MULTIPLE FILES
            files = request.FILES.getlist('file')
            for f in files:
                CommentAttachment.objects.create(
                    comment=comment,
                    file=f
                )

            # 👉 пользователь становится участником
            topic.participants.add(request.user)

            return redirect(f'/topic/{topic.id}/')

    return render(request, 'comments/add_comment.html', {
        'form': form,
        'topic': topic
    })
