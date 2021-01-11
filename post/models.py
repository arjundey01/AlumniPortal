from users.models import Account
from django.db import models
from django_editorjs import EditorJsField
import datetime
# Create your models here.
# class Post(models.Model):
#     author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',null=True)
#     text=models.CharField(max_length=1000, null=True)
#     datetime=models.DateTimeField(auto_now_add=True)
#     likess=models.ManyToManyField(User,related_name='likes')
#     @property
#     def rev_priority(self):
#         age=(datetime.datetime.now()-self.datetime).total_seconds()//(3600*24)
#         likes_count=len(self.likes.all())
#         #in every 3 day group, the priority is decided by likes 
#         return age//3 + 1/(likes_count or 1)




# class Like(models.Model):
#     post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    # author=models.CharField(max_length=50)

class Post(models.Model):
    author=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='posts',null=True)
    datetime=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(Account,related_name='liked_posts')
    content=EditorJsField(
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
    @property
    def rev_priority(self):
        age=(datetime.datetime.now()-self.datetime).total_seconds()//(3600*24)
        likes_count=len(self.likes.all())
        #in every 3 day group, the priority is decided by likes 
        return age//3 + 1/(likes_count or 1)

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',null=True)
    author=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='comments',null=True)
    content=models.CharField(max_length=500, null=True)
    create_date=models.DateTimeField(auto_now_add=True)