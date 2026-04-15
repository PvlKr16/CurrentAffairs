from django.contrib.auth import login, logout
from .forms import LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User
from django import forms


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home/')  # НЕ на "/"

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/home/')

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login/')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']


@login_required
def contacts_page(request):
    if request.user.is_guest:
        return redirect('/home/')

    users = User.objects.all().order_by('first_name', 'last_name')
    return render(request, 'users/contacts.html', {'users': users})


@login_required
def profile_page(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    is_owner = request.user == profile_user

    avatar_form = ProfileForm(instance=profile_user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST' and is_owner:

        if 'save_avatar' in request.POST:
            avatar_form = ProfileForm(
                request.POST,
                request.FILES,
                instance=profile_user
            )
            if avatar_form.is_valid():
                avatar_form.save()
                return redirect(f'/profile/{user_id}/')

        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(
                request.user,
                request.POST
            )
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect(f'/profile/{user_id}/')

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'is_owner': is_owner,
        'avatar_form': avatar_form,
        'password_form': password_form,
    })

@login_required
@require_POST
def change_theme(request):
    theme = request.POST.get('theme')

    allowed = ['emerald', 'ultramarine', 'violet_orange']

    if theme in allowed:
        request.user.color_scheme = theme
        request.user.save()
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})
