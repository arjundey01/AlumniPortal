from django.urls import path,include
from .views import *

app_name = 'events'

urlpatterns = [
    path('', events,name='events'),
    path('event/<id>/',eventPage,name='event'),
    path('save/', save_event, name='save-event'),
    path('interested/', interested_event, name='interested-event'),
    path('delete/<id>/', delete_event, name='delete-event'),
    path('create-edit/', create_edit_event, name='create-edit-event'),
]