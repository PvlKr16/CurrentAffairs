from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import CommentForm
from topics.models import Topic, TopicReadStatus


@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    initial = {}
    quote = request.GET.get('quote', '').strip()

    if quote:
        initial['title'] = quote[:255]

    form = CommentForm(
        request.POST or None,
        request.FILES or None,
        initial=initial
    )

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.topic = topic
            comment.save()

            TopicReadStatus.objects.update_or_create(
                user=request.user,
                topic=topic,
                defaults={'last_read_at': timezone.now()}
            )

            return redirect(f'/topic/{topic.id}/')

    return render(request, 'comments/add_comment.html', {
        'form': form,
        'topic': topic
    })
