from django.shortcuts import render, redirect
from .forms import TopicCreateForm
from django.contrib.auth.decorators import login_required
from .models import Topic
from django.shortcuts import get_object_or_404
from comments.models import Comment
from .models import Topic, TopicReadStatus
from django.utils import timezone


def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_guest:
            return redirect('/home/')
        return view_func(request, *args, **kwargs)
    return wrapper



@login_required
@guest_required
def create_topic(request):
    form = TopicCreateForm(request.POST or None, user=request.user)

    if request.method == 'POST':
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()

            form.save_m2m()

            # Ensure author is participant
            topic.participants.add(request.user)

            return redirect('/home/')

    return render(request, 'topics/create_topic.html', {'form': form})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Access control
    if not topic.is_open and request.user not in topic.participants.all():
        return redirect('/home/')

    comments = topic.comments.all().order_by('created_at')

    # Mark as read
    TopicReadStatus.objects.update_or_create(
        user=request.user,
        topic=topic,
        defaults={'last_read_at': timezone.now()}
    )

    return render(request, 'topics/topic_detail.html', {
        'topic': topic,
        'comments': comments
    })

def mark_unread(request, topic_id):
    TopicReadStatus.objects.filter(
        user=request.user,
        topic_id=topic_id
    ).delete()

    return redirect('/home/')
