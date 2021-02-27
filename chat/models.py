from django.db import models
from users.models import Account
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import json
class Chats(models.Model):
    group_name=models.CharField(primary_key=True,null=False,max_length=100)
    data=models.TextField(null=True)
    members=models.ManyToManyField(Account,related_name='chats')
    last_seen_msg=models.TextField(null=True)
    def save(self, *args, **kwargs):
        print('saving Chat...',self.data)
        super().save(*args, **kwargs) 
    
    @property
    def age(self):
        chat_data = json.loads(self.data)
        if len(chat_data):
            age=datetime.now() - datetime.fromisoformat(chat_data[-1]['time'])
            return age.seconds    
        else:
            return -1
    @property
    def last_msg(self):
        chat_data = json.loads(self.data)
        if len(chat_data):
            return chat_data[-1]
        else:
            return None