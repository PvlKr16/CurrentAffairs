from django import forms
from .models import Topic
from django.contrib.auth import get_user_model

User = get_user_model()


class TopicCreateForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Topic
        fields = ['title', 'description', 'content', 'is_open', 'participants']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['participants'].queryset = User.objects.exclude(id=user.id)
