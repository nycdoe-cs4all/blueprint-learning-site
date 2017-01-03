from django import forms

from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'subject', 'html_body', 'plain_body', 'grade']

