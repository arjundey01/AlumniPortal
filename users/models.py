from django.db import models
from django.contrib.auth.models import User
import re
from datetime import datetime
# Create your models here.

def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.user.username:
        return 'images/profile_imgs/'+'{}_{}.{}'.format(instance.user.username,re.sub(r'[^\w]', '', "%s"%(datetime.now().time())) ,ext)

class Account(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    following=models.ManyToManyField('Account',related_name='followers', blank=True)
    profile_img=models.ImageField(upload_to=profile_image_path,null=True)
    last_active=models.DateTimeField(null=True,default=datetime.now)
    @property
    def profile_img_url(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return "/static/img/default-avatar.svg"