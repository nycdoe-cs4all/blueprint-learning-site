from django import forms

from .models import Activity, Profile, Resource


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'subject', 'html_body', 'plain_body', 'grade']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'school', 'organization', 'link']
        labels = {
            'organization': 'Other Organization',
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'body', 'activities', 'tags']
