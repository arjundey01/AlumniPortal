from users.models import Account
from django.db import models

from groups.models import Group

import datetime

class Question(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField(blank=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Group, related_name='questions')
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
    posted_on = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(Account,related_name='upvoted_answer')
    downvotes = models.ManyToManyField(Account,related_name='downvoted_answer')
    accepted = models.BooleanField(default=False)
    content = models.TextField(blank=False)

    def __str__(self) -> str:
        return self.author.name + "_q:" + str(self.question.id) + "_" + str(self.id)

    @property
    def rev_priority(self):
        if self.accepted:
            return 1
        return 2 + 1 / (self.upvotes.all().count() or 1)

    def upvote_count(self):
        return self.upvotes.all().count()

    def downvote_count(self):
        return self.downvotes.all().count()
    


