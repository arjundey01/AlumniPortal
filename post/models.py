from django.core.exceptions import ValidationError
from users.models import Account
from django.db import models
from .editorjsmod import EditorJsFieldMod
from groups.models import Group
import datetime
import json
class Post(models.Model):
    author=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='posts',null=True)
    datetime=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(Account,related_name='liked_posts')
    tags=models.ManyToManyField(Group, related_name='posts')
    content_old=EditorJsFieldMod(
        editorjs_config={
            "tools":{
                "Image":{
                    "config":{
                        "endpoints":{
                            "byFile":'http://localhost:8000/post/feign-imageUpload/',
                            "byUrl":'http://localhost:8000/post/feign-imageUpload/',
                        },
                        "additionalRequestHeaders":[{"Content-Type":'multipart/form-data'}]
                    }
                },
                "Attaches":{
                    "config":{
                        "endpoint":'http://localhost:8000/post/feign-fileUpload/'
                    }
                }
            },
            "logLevel":"ERROR"
        },null=True)
    content=models.JSONField(default=dict)
    @property
    def rev_priority(self):
        age=(datetime.datetime.now()-self.datetime).total_seconds()//(3600*24)
        likes_count=len(self.likes.all())
        #in every 3 day group, the priority is decided by likes 
        return age//3 + 1/(likes_count or 1)

    def __str__(self):
        return self.author.name + "_" + str(self.id) 

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',null=True)
    author=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='comments',null=True)
    content=models.CharField(max_length=500, null=True)
    create_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.name + "_" + str(self.post.id) + '_' + str(self.id) 
