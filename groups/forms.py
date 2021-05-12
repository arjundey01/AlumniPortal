from django.db.models import fields
from .models import Group
from django import forms

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title','cover_image']