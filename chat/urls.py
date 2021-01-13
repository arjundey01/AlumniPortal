from django.urls import path,include
from . import views

urlpatterns = [
    path(r't/<room_name>/',views.chatroom),
    path(r'start/',views.start_chat),
    path(r'online/',views.get_online),
    path(r'last-active/',views.get_last_active),
]