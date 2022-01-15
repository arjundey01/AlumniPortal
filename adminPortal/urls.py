from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('accounts/', accounts),
    path('posts/', posts),
    path('accounts/delete/<id>', delete_account),
    path('posts/delete/<id>', delete_post),
]
