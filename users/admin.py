from django.contrib import admin
from .models import Account, Education, Experience, Organization,Designation, PastJobs, Project
# Register your models here.
admin.site.register(Account)
admin.site.register(Organization)
admin.site.register(Designation)
admin.site.register(Experience)
admin.site.register(PastJobs)
admin.site.register(Project)
admin.site.register(Education)