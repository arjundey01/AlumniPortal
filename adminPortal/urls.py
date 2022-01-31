from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='admin'),
    path('accounts/', accounts),
    path('posts/', posts),
    path('groups/', groups),
    path('events/', events),
    path('faqs/', faqs),
    path('accounts/delete/<id>/', delete_account),
    path('posts/delete/<id>/', delete_post),
    path('groups/delete/<id>/', delete_group),
    path('events/delete/<id>/', delete_event),
    path('faqs/delete/<id>/', delete_faq),
]
