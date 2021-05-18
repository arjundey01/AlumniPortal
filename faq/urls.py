from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ,name='faq'),
    path('create-question/', views.create_question, name='create_question'),
    path('load-question/<index>', views.load_question, name='load_question'),
]