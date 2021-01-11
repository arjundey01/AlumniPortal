from django.contrib import admin
from django.urls import path, re_path ,include
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='post'

urlpatterns=[
    path('', views.index ,name='wall'),
    path('create-post/', views.create_post ,name='create_post'),
    path('delete/<pk>/', views.delete_post ,name='post_delete'),
    path('update/<pk>/', views.update_post ,name='post_update'),
    path('detail/<pk>', views.post_details, name='post_detail'),
    path('load-feed/<index>',views.load_feed),
    path('feed/',views.feed, name='feed'),
    path('like-post/',views.like_post, name='like-post'),
    path('fileUpload/', csrf_exempt(views.upload_file_view)),
    path('feign-fileUpload/', csrf_exempt(views.feign_file_upload)),
    path('imageUpload/', csrf_exempt(views.upload_image_view)),
    path('feign-imageUpload/', csrf_exempt(views.feign_image_upload)),
]