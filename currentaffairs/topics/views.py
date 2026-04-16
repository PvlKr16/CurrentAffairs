from django.shortcuts import render, redirect
from .forms import TopicCreateForm, PollForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from comments.models import Comment
from .models import Topic, TopicReadStatus, Poll, PollOption, PollVote
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

    # Visible topics
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
            poll.save()
            form.save_m2m()

            poll.participants.add(request.user)

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

    if not poll.is_open and request.user not in poll.participants.all():
        return redirect('/home/')

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
    })


@login_required
def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

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

    return redirect(f'/poll/{poll.id}/')
