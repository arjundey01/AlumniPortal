from .models import Post, Comment
from django import forms
from django_editorjs import EditorJsField
from groups.models import Group

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), label='', required = False)
    class Meta():
        model=Post
        fields=['content','tags']
        labels={'content':'','tags':''}

class CommentForm(forms.ModelForm):
    content= forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': ''}))
    class Meta:
        model=Comment
        fields=['content']
        labels={'content':''}
