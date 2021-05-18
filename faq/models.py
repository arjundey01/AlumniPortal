from users.models import Account
from django.db import models

import datetime

class Question(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField(blank=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.author.name + "_" + str(self.id)

    @property
    def ans_count(self):
        return len(self.answers.all())

    @property
    def rev_priority(self):
        timediff = datetime.datetime.now() - self.posted_on
        return timediff.total_seconds()//3600 + 1 / (self.views or 1)


class Answer(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    upvotes = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    content = models.TextField(blank=False)

    def __str__(self) -> str:
        return self.author.name + "_q:" + str(self.question.id) + "_" + str(self.id)

    @property
    def rev_priority(self):
        if self.accepted:
            return 1
        return 2 + 1 / (self.upvotes or 1)
