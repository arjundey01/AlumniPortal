from django.contrib import admin
from .models import Account, Organization,Designation,Contact,Education,Experience,PastJobs,Project
# Register your models here.
admin.site.register(Account)
admin.site.register(Organization)
admin.site.register(Designation)
admin.site.register(Contact)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(PastJobs)
admin.site.register(Project)
