from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.utils.translation import gettext_lazy as _


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'is_guest', 'native_language']
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'password': _('Password'),
            'is_guest': _('Guest'),
            'native_language': _('Native language'),
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
