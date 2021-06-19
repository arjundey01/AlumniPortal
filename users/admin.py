from django.contrib import admin
from .models import Account, Organization,Designation
# Register your models here.
admin.site.register(Account)
admin.site.register(Organization)
admin.site.register(Designation)