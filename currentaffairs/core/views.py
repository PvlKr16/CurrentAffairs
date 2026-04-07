from django.shortcuts import redirect
from django.http import HttpResponse


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('/home/')  # пока заглушка
    return redirect('/login/')

def home_view(request):
    return HttpResponse("HOME PAGE (temporary)")
