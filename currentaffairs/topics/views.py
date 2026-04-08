from django.shortcuts import render, redirect
from .forms import TopicCreateForm
from django.contrib.auth.decorators import login_required
from .models import Topic


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
