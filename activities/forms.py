from django import forms

from .models import Activity, Profile


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'subject', 'html_body', 'plain_body', 'grade']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'organization', 'link']

