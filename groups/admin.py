from django.contrib import admin
from .models import Group
# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    model = Group
    filter_horizontal = ('members',)

admin.site.register(Group, GroupAdmin)