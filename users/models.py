from django.db import models
from django.db.models.fields import related
from django.contrib.auth.models import User
from django.utils import tree
# Create your models here.
class Account(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    following=models.ManyToManyField('Account',related_name='followers')