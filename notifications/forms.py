from django import forms
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()
class NotificationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        empty_label="Select a student",
        required=True
    )
    class Meta:
        model = Notification
        fields = ['title', 'message', 'category', 'user']
