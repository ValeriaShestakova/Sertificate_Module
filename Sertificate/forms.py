from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_number', 'begin_date', 'end_date', 'program', 'teacher']
