from django.db import models
from datetime import datetime, date, time
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Account


class Event(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    event_time = models.DateTimeField()
    cover_image = models.ImageField(upload_to = 'images/events', blank=True, null=True)
    saved_by = models.ManyToManyField(Account, related_name='saved_events', blank=True)
    interested_users = models.ManyToManyField(Account, related_name='interested_events', blank=True)
    
    def __str__(self):
        return self.title

    @property
    def cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        else:
            return "/static/img/events-bg.png"