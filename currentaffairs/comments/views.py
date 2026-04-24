from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse

from .forms import CommentForm
from .models import Comment, CommentAttachment
from topics.models import Topic, TopicReadStatus


@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.user.is_guest and request.user not in topic.participants.all():
        return redirect('/home/')

    if not topic.is_open and request.user not in topic.participants.all():
        return redirect('/home/')

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

@login_required
def comments_json(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    comments = topic.comments.select_related('author').order_by('created_at')

    data = []

    for c in comments:
        data.append({
            'id': c.id,
            'author': f"{c.author.first_name} {c.author.last_name}",
            'content': c.content,
            'created_at': c.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({'comments': data})
