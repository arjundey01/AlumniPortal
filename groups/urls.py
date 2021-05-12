from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('', views.all_groups ,name='groups'),
    path('create/', csrf_exempt(views.create_group) ,name='create'),
    path('delete/<id>/', csrf_exempt(views.delete_group) ,name='delete'),
    path('rename/<id>/', csrf_exempt(views.rename_group) ,name='rename'),
    path('change-cover/<id>/', csrf_exempt(views.change_cover_group), name='change_cover'),
    path('join-group/<id>/', csrf_exempt(views.join_group), name='join'),
    path('leave-group/<id>/', csrf_exempt(views.leave_group), name='leave'),
    path('get-members/<id>/', csrf_exempt(views.get_members), name='members'),

]