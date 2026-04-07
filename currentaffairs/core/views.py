from django.shortcuts import redirect, render
from topics.models import Topic


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    return redirect('/login/')

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    topics = Topic.objects.all().order_by('-updated_at')

    return render(request, 'core/home.html', {
        'topics': topics
    })
