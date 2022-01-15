from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('accounts/', accounts),
    path('posts/', posts),
    path('groups/', groups),
    path('accounts/delete/<id>', delete_account),
    path('posts/delete/<id>', delete_post),
    path('groups/delete/<id>', delete_group),
]
