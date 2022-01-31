from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name="groups"

urlpatterns=[
    path('', views.all_groups ,name='groups'),
    path('page/<id>/',views.group,name='group'),
    path('create-edit/', csrf_exempt(views.create_edit_group) ,name='create'),
    path('delete/<id>/', csrf_exempt(views.delete_group) ,name='delete'),
    path('rename/<id>/', csrf_exempt(views.rename_group) ,name='rename'),
    path('change-cover/<id>/', csrf_exempt(views.change_cover_group), name='change_cover'),
    path('join-group/<id>/', csrf_exempt(views.join_group), name='join'),
    path('leave-group/<id>/', csrf_exempt(views.leave_group), name='leave'),
    path('get-members/<id>/', csrf_exempt(views.get_members), name='members'),
]