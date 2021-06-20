from django.db.models import fields
from .models import Answer, Question
from django import forms

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
