from django.db import models

# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length = 75)
    cover_image = models.ImageField(upload_to = 'images/groups', blank=True, null=True)

    def __str__(self):
        return self.title
    