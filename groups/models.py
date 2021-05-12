from django.db import models
from users.models import Account
# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length = 75)
    cover_image = models.ImageField(upload_to = 'images/groups', blank=True, null=True)
    members = models.ManyToManyField(Account, related_name='groups')
    
    def __str__(self):
        return self.title
    
    @property 
    def member_count(self):
        return len(self.members.all())