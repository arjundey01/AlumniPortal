from django.contrib import admin
from django.urls import path, re_path ,include
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='post'

urlpatterns=[
    path('create-post/', views.create_post ,name='create_post'),
    path('delete/', csrf_exempt(views.delete_post) ,name='post_delete'),
    path('update/<pk>/', views.update_post ,name='post_update'),
    path('detail/<pk>', views.post_details, name='post_detail'),
    path('load-feed/<index>',views.load_feed),
    path('load-post/<id>',views.individual_post),
    path('like-post/',views.like_post, name='like-post'),
    path('fileUpload/', csrf_exempt(views.upload_file_view)),
    path('imageUpload/', csrf_exempt(views.upload_image_view)),
    path('comment/<pk>/', views.comment, name='comment'),
    path('load-comment/<id>', views.load_comment),
    path('load-likes/<id>', views.load_likes),
]