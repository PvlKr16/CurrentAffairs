from django.shortcuts import render, redirect
from .forms import TopicCreateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from comments.models import Comment
from .models import Topic, TopicReadStatus
from django.db.models import Max
from django.http import JsonResponse
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

            # Author is always participant
            topic.participants.add(request.user)

            # Mark topic as read for author immediately
            TopicReadStatus.objects.update_or_create(
                user=request.user,
                topic=topic,
                defaults={'last_read_at': timezone.now()}
            )

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

def get_unread_topics_for_user(user):
    if not user.is_authenticated:
        return Topic.objects.none()

    topics = Topic.objects.filter(participants=user)

    unread_ids = []

    for topic in topics:
        status = TopicReadStatus.objects.filter(
            user=user,
            topic=topic
        ).first()

        latest_comment = topic.comments.order_by('-created_at').first()

        latest_activity = topic.created_at
        if latest_comment:
            latest_activity = latest_comment.created_at

        if not status:
            unread_ids.append(topic.id)
        elif latest_activity > status.last_read_at:
            # Ignore own comment
            if latest_comment and latest_comment.author == user:
                continue
            unread_ids.append(topic.id)

    return Topic.objects.filter(id__in=unread_ids)

def unread_count_api(request):
    unread = get_unread_topics_for_user(request.user)
    return JsonResponse({
        'count': unread.count()
    })

def unread_topics_page(request):
    topics = get_unread_topics_for_user(request.user)

    sort = request.GET.get('sort', 'newest')

    topics = list(topics)

    topics.sort(
        key=lambda t: t.comments.order_by('-created_at').first().created_at
        if t.comments.exists()
        else t.created_at,
        reverse=(sort == 'newest')
    )

    return render(request, 'topics/unread_topics.html', {
        'topics': topics,
        'sort': sort
    })
