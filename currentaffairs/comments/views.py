from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from topics.models import Topic
from django.contrib.auth.decorators import login_required


@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.topic = topic
            comment.save()

            return redirect(f'/topic/{topic.id}/')

    return render(request, 'comments/add_comment.html', {'form': form})
