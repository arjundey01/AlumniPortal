from django.db import models
from users.models import Account

class Chats(models.Model):
    group_name=models.CharField(primary_key=True,null=False,max_length=100)
    data=models.TextField(null=True)
    members=models.ManyToManyField(Account,related_name='chats')
    last_seen_msg=models.TextField(null=True)

