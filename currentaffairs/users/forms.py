from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'is_guest']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
