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

class Experience(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, related_name="experiences")
    experience=models.CharField(max_length=100)

class Project(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, related_name="projects")
    project=models.CharField(max_length=100)

class Education(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, related_name="educations")
    education=models.CharField(max_length=100)
    
class Contact(models.Model):
     user=models.OneToOneField(Account, on_delete=models.CASCADE, related_name="contact")
     gmail=models.EmailField(blank=True, null=True)
     outlook=models.EmailField(blank=True, null=True)
     linkedin=models.URLField(blank=True, null=True)
     mobile=models.IntegerField(blank=True, null=True)