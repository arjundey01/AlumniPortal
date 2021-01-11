from .models import Post, Comment
from django import forms
from django_editorjs import EditorJsField

class PostForm(forms.ModelForm):
    class Meta():
        model=Post
        fields=['content']
        labels={'content':''}

class CommentForm(forms.ModelForm):
    content= forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': ''}))
    class Meta:
        model=Comment
        fields=['content']
        labels={'content':''}
