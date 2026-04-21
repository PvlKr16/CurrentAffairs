from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import CommentForm
from .models import Comment
from topics.models import Topic, TopicReadStatus


@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Only participants see closed topic
    if not topic.is_open and request.user not in topic.participants.all():
        return redirect('/home/')

    initial = {}

    quote = request.GET.get('quote', '').strip()
    if quote:
        initial['content'] = f'> {quote}\n\n'

    form = CommentForm(
        request.POST or None,
        request.FILES or None,
        initial=initial
    )

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()

            # User is added to participants after he added comment
            topic.participants.add(request.user)

            # Topic is marked as read at once
            TopicReadStatus.objects.update_or_create(
                user=request.user,
                topic=topic,
                defaults={'last_read_at': timezone.now()}
            )

            return redirect(f'/topic/{topic.id}/')

    return render(request, 'comments/add_comment.html', {
        'form': form,
        'topic': topic,
    })
