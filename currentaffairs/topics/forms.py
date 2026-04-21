from django import forms
from .models import Topic, Poll
from users.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TopicCreateForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-select'}
        )
    )

    class Meta:
        model = Topic
        fields = [
            'title',
            'description',
            'content',
            'file',
            'is_open',
            'participants'
        ]
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'content': _('Content'),
            'file': _('File'),
            'is_open': _('Open'),
            'participants': _('Participants')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['participants'].queryset = (
                User.objects.exclude(id=user.id)
            )


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            'question',
            'file',
            'is_open',
            'is_anonymous',
            'allow_multiple',
            'participants'
        ]
        labels = {
            'question': _('Question'),
            'file': _('File'),
            'is_open': _('Open'),
            'is_anonymous': _('Anonymous'),
            'allow_multiple': _('Allow multiple'),
            'participants': _('Participants')
        }

        widgets = {
            'participants': forms.SelectMultiple(
                attrs={'class': 'form-select'}
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['participants'].queryset = User.objects.exclude(
                id=user.id
            )
