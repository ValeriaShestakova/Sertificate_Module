from django import forms
from .models import Group, User
from userprofile.models import UserProfile


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_number', 'begin_date', 'end_date', 'program', 'teacher']

