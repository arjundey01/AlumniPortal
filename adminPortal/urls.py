from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('accounts/', accounts),
    path('posts/', posts),
]
