from users.models import Account
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField(blank=False)
    views = models.IntegerField(default=0)

class Answer(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='answers')
    upvotes = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    content = models.TextField(blank=False)

