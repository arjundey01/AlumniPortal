from django.db import models
from datetime import datetime, date, time
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    event_date = models.DateField(auto_now_add=False,auto_now=False,blank=True)
    event_time = models.TimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    
    def __str__(self):
        return self.title