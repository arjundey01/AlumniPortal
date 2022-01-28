from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.events,name='events'),
    path('eventpage',views.eventPage,name='eventPage'),
]