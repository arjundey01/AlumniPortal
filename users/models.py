from django.db import models
from django.contrib.auth.models import User
import re
from datetime import date, datetime
# Create your models here.

def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.user.username:
        return 'images/profile_imgs/'+'{}_{}.{}'.format(instance.user.username,re.sub(r'[^\w]', '', "%s"%(datetime.now().time())) ,ext)

class Account(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    name=models.CharField(max_length=100)
    email=models.EmailField()
    following=models.ManyToManyField('Account',related_name='followers', blank=True)
    profile_img=models.ImageField(upload_to=profile_image_path,null=True)
    last_active=models.DateTimeField(null=True,default=datetime.now)
    organization=models.ManyToManyField('Organization',related_name='employees')
    designation = models.ManyToManyField('Designation',related_name='employees')
    pastjobs = models.ManyToManyField('PastJobs',related_name='employees')
    is_alumni = models.BooleanField(default=False)
    @property
    def profile_img_url(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return "/static/img/default-avatar.svg"

    def __str__(self):
        return self.name

class Experience(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, related_name="experiences")
    experience=models.CharField(max_length=100)
    start_date=models.DateField(default=date.today)
    end_date=models.DateField(null=True, blank=True)

    def get_duration(self):
        duration={}
        # months = (self.end_date.year - self.start_date.year)*12+ (self.end_date.month - self.start_date.month)
        duration["years"]=(self.end_date.year - self.start_date.year)
        duration["months"]=(self.end_date.month - self.start_date.month)
        return duration

    def get_start_date(self):
        if(self.start_date):
            return self.start_date
        else:
            return date.today()

    def get_end_date(self):
        if(self.end_date):
            return self.end_date
        else:
            return False

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

class Organization(models.Model):
    name=models.CharField(max_length=150)

class Designation(models.Model):
    title=models.CharField(max_length=150)

class PastJobs(models.Model):
    organization=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="jobs")
    designation=models.ForeignKey(Designation,on_delete=models.CASCADE, related_name="jobs")
    start_date=models.DateField(default=date.today)
    end_date=models.DateField(null=True, blank=True)

    def get_duration(self):
        duration={}
        # months = (self.end_date.year - self.start_date.year)*12+ (self.end_date.month - self.start_date.month)
        duration["years"]=(self.end_date.year - self.start_date.year)
        duration["months"]=(self.end_date.month - self.start_date.month)
        return duration

    def get_start_date(self):
        if(self.start_date):
            return self.start_date
        else:
            return date.today()

    def get_end_date(self):
        if(self.end_date):
            return self.end_date
        else:
            return False
