from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from comments.models import Comment
from .forms import TopicCreateForm, PollForm
from .models import (
    Topic,
    TopicReadStatus,
    TopicAttachment,
    Poll,
    PollOption,
    PollVote,
    PollReadStatus,
    PollAttachment
)

User = get_user_model()

def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_guest:
            return redirect('/home/')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@guest_required
def create_topic(request):
    form = TopicCreateForm(
        request.POST or None,
        request.FILES or None,
        user=request.user
    )

    if request.method == 'POST':
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user

            # ❗ отключаем старое поле file
            topic.file = None

            topic.save()
            form.save_m2m()

            # Автор всегда участник
            topic.participants.add(request.user)

            # ✅ СОХРАНЕНИЕ MULTIPLE FILES
            files = request.FILES.getlist('file')
            for f in files:
                TopicAttachment.objects.create(
                    topic=topic,
                    file=f
                )

            TopicReadStatus.objects.update_or_create(
                user=request.user,
                topic=topic,
                defaults={'last_read_at': timezone.now()}
            )

            return redirect('/home/')

    return render(request, 'topics/create_topic.html', {
        'form': form
    })


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.user.is_guest and request.user not in topic.participants.all():
        return redirect('/home/')

    if not topic.is_open and request.user not in topic.participants.all():
        return redirect('/home/')

    comments = topic.comments.all().order_by('created_at')

    TopicReadStatus.objects.update_or_create(
        user=request.user,
        topic=topic,
        defaults={'last_read_at': timezone.now()}
    )

    is_participant = topic.participants.filter(
        id=request.user.id
    ).exists()

    return render(request, 'topics/topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'is_participant': is_participant,
        'users': User.objects.exclude(id=request.user.id),
    })

@login_required
@require_POST
def follow_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.user.is_guest:
        return redirect('/home/')

    topic.participants.add(request.user)

    TopicReadStatus.objects.update_or_create(
        user=request.user,
        topic=topic,
        defaults={'last_read_at': timezone.now()}
    )

    return redirect(f'/topic/{topic.id}/')

@login_required
@require_POST
def unfollow_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.user == topic.author:
        return redirect(f'/topic/{topic.id}/')

    topic.participants.remove(request.user)

    TopicReadStatus.objects.filter(
        user=request.user,
        topic=topic
    ).delete()

    return redirect('/home/')

@login_required
def mark_unread(request, topic_id):
    TopicReadStatus.objects.filter(
        user=request.user,
        topic_id=topic_id
    ).delete()

    return redirect('/home/')


# ==================================================
# UNREAD LOGIC
# ==================================================

def get_unread_topics_for_user(user):
    if not user.is_authenticated:
        return []

    unread = []

    # ---------------- Topics ----------------
    topics = Topic.objects.filter(participants=user)

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
            unread.append({
                'type': 'topic',
                'obj': topic,
                'title': topic.title,
                'updated': latest_activity,
            })

        elif latest_activity > status.last_read_at:
            if latest_comment and latest_comment.author == user:
                continue

            unread.append({
                'type': 'topic',
                'obj': topic,
                'title': topic.title,
                'updated': latest_activity,
            })

    # ---------------- Polls ----------------
    polls = Poll.objects.filter(participants=user)

    for poll in polls:
        status = PollReadStatus.objects.filter(
            user=user,
            poll=poll
        ).first()

        last_vote = poll.votes.exclude(
            user=user
        ).order_by('-created_at').first()

        latest_activity = poll.created_at
        if last_vote:
            latest_activity = last_vote.created_at

        if not status:
            unread.append({
                'type': 'poll',
                'obj': poll,
                'title': f'POLL: {poll.question}',
                'updated': latest_activity,
            })

        elif latest_activity > status.last_read_at:
            unread.append({
                'type': 'poll',
                'obj': poll,
                'title': f'POLL: {poll.question}',
                'updated': latest_activity,
            })

    return unread


@login_required
def unread_count_api(request):
    unread = get_unread_topics_for_user(request.user)

    return JsonResponse({
        'count': len(unread)
    })


@login_required
def unread_topics_page(request):
    items = get_unread_topics_for_user(request.user)

    sort = request.GET.get('sort', 'newest')

    items.sort(
        key=lambda x: x['updated'],
        reverse=(sort == 'newest')
    )

    return render(request, 'topics/unread_topics.html', {
        'items': items,
        'sort': sort
    })


# ==================================================
# SEARCH
# ==================================================

@login_required
def search_topics(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('/home/')

    by_author = request.GET.get('author')
    in_title = request.GET.get('title')
    in_description = request.GET.get('description')
    in_content = request.GET.get('content')
    in_comments = request.GET.get('comments')
    by_date = request.GET.get('date')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    user = request.user

    if user.is_guest:
        topics = Topic.objects.filter(participants=user)
    else:
        topics = Topic.objects.filter(
            Q(is_open=True) | Q(participants=user)
        ).distinct()

    filters = Q()

    if by_author:
        filters |= Q(author__first_name__icontains=query)
        filters |= Q(author__last_name__icontains=query)
        filters |= Q(author__email__icontains=query)

    if in_title:
        filters |= Q(title__icontains=query)

    if in_description:
        filters |= Q(description__icontains=query)

    if in_content:
        filters |= Q(content__icontains=query)

    if in_comments:
        filters |= Q(comments__content__icontains=query)

    if by_date:
        if date_from:
            filters &= Q(created_at__gte=date_from)

        if date_to:
            filters &= Q(created_at__lte=date_to)

    results = topics.filter(filters).distinct()

    return render(request, 'topics/search_results.html', {
        'topics': results,
        'query': query
    })


# ==================================================
# POLLS
# ==================================================

@login_required
def create_poll(request):
    if request.user.is_guest:
        return redirect('/home/')

    if request.method == 'POST':
        form = PollForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        options = request.POST.getlist('options')

        if form.is_valid():
            poll = form.save(commit=False)
            poll.author = request.user

            # ❗ отключаем старое поле
            poll.file = None

            poll.save()
            form.save_m2m()

            poll.participants.add(request.user)

            # ✅ MULTIPLE FILES
            files = request.FILES.getlist('file')
            for f in files:
                PollAttachment.objects.create(
                    poll=poll,
                    file=f
                )

            PollReadStatus.objects.update_or_create(
                user=request.user,
                poll=poll,
                defaults={'last_read_at': timezone.now()}
            )

            for text in options:
                text = text.strip()
                if text:
                    PollOption.objects.create(
                        poll=poll,
                        text=text
                    )

            return redirect(f'/poll/{poll.id}/')

    else:
        form = PollForm(user=request.user)

    return render(request, 'topics/create_poll.html', {
        'form': form
    })


@login_required
def view_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user.is_guest and request.user not in poll.participants.all():
        return redirect('/home/')

    if not poll.is_open and request.user not in poll.participants.all():
        return redirect('/home/')

    PollReadStatus.objects.update_or_create(
        user=request.user,
        poll=poll,
        defaults={'last_read_at': timezone.now()}
    )

    voted = PollVote.objects.filter(
        poll=poll,
        user=request.user
    ).exists()

    waiting = poll.participants.exclude(
        id__in=poll.votes.values_list('user_id', flat=True)
    )

    return render(request, 'topics/view_poll.html', {
        'poll': poll,
        'voted': voted,
        'waiting': waiting,
        'users': User.objects.exclude(id=request.user.id),
    })


@login_required
def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user.is_guest:
        return redirect('/home/')

    if request.user not in poll.participants.all():
        return redirect(f'/poll/{poll.id}/')

    if not poll.is_open and request.user not in poll.participants.all():
        return redirect('/home/')

    already = PollVote.objects.filter(
        poll=poll,
        user=request.user
    ).exists()

    if already:
        return redirect(f'/poll/{poll.id}/')

    selected = request.POST.getlist('options')

    if not poll.allow_multiple:
        selected = selected[:1]

    for option_id in selected:
        option = get_object_or_404(
            PollOption,
            id=option_id,
            poll=poll
        )

        PollVote.objects.create(
            poll=poll,
            option=option,
            user=request.user
        )

    # Own vote must not create unread
    PollReadStatus.objects.update_or_create(
        user=request.user,
        poll=poll,
        defaults={'last_read_at': timezone.now()}
    )

    return redirect(f'/poll/{poll.id}/')


@login_required
def poll_results_api(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    data = []

    for option in poll.options.all():

        votes = PollVote.objects.filter(
            poll=poll,
            option=option
        )

        count = votes.count()

        users = []

        if not poll.is_anonymous:
            users = list(
                votes.select_related('user').values_list(
                    'user__first_name',
                    'user__last_name'
                )
            )

        data.append({
            'id': option.id,
            'text': option.text,
            'count': count,
            'users': users,
        })

    total_users = poll.participants.count()
    voted_users = poll.votes.values('user').distinct().count()

    completed = total_users > 0 and voted_users >= total_users

    waiting = list(
        poll.participants.exclude(
            id__in=poll.votes.values_list('user_id', flat=True)
        ).values_list('first_name', 'last_name')
    )

    return JsonResponse({
        'results': data,
        'completed': completed,
        'waiting': waiting,
        'anonymous': poll.is_anonymous,
    })

# Participants

@login_required
def add_topic_participant(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.user not in topic.participants.all():
        return redirect(f'/topic/{topic.id}/')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        if user_id:
            user = get_object_or_404(User, id=user_id)
            topic.participants.add(user)

    return redirect(f'/topic/{topic.id}/')


@login_required
def leave_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.user != topic.author:
        topic.participants.remove(request.user)

    return redirect('/home/')


@login_required
def add_poll_participant(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user not in poll.participants.all():
        return redirect(f'/poll/{poll.id}/')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        if user_id:
            user = get_object_or_404(User, id=user_id)
            poll.participants.add(user)

    return redirect(f'/poll/{poll.id}/')


@login_required
def leave_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user != poll.author:
        poll.participants.remove(request.user)

    return redirect('/home/')
