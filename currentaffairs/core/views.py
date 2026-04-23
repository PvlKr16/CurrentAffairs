from django.shortcuts import redirect, render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from topics.models import Topic, Poll, PollVote, TopicReadStatus
# from comments.models import TopicReadStatus


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    return redirect('/login/')


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    user = request.user
    items = []

    # Topics
    if user.is_guest:
        topics = Topic.objects.filter(
            participants=user
        )
    else:
        topics = Topic.objects.filter(
            Q(is_open=True) | Q(participants=user)
        ).distinct()

    for topic in topics:
        items.append({
            'type': 'topic',
            'obj': topic,
            'title': topic.title,
            'updated': topic.updated_at,
        })

    # Polls
    if user.is_guest:
        polls = Poll.objects.filter(
            participants=user
        )
    else:
        polls = Poll.objects.filter(
            Q(is_open=True) | Q(participants=user)
        ).distinct()

    for poll in polls:
        items.append({
            'type': 'poll',
            'obj': poll,
            'title': f'POLL: {poll.question}',
            'updated': poll.created_at,
        })

    items.sort(
        key=lambda x: x['updated'],
        reverse=True
    )

    return render(request, 'core/home.html', {
        'items': items
    })

# Live HOME
@login_required
def home_json(request):
    user = request.user
    items = []

    if user.is_guest:
        topics = Topic.objects.filter(participants=user)
    else:
        topics = Topic.objects.filter(
            Q(is_open=True) | Q(participants=user)
        ).distinct()

    for topic in topics:
        items.append({
            'id': topic.id,
            'title': topic.title,
            'updated': topic.updated_at.strftime("%Y-%m-%d %H:%M"),
            'type': 'topic'
        })

    return JsonResponse({'items': items})
