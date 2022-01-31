from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.index ,name='faq'),
    path('create-question/', views.create_question, name='create_question'),
    path('load-question/<index>', views.load_question, name='load_question'),
    path('question/<id>/', views.question_detail, name='detail_question'),
    path('create-ans/<id>/', views.create_answer, name='create_answer'),
    path('ans-from-alumni', views.get_best4, name='ans-from-alumni'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
    path('accept-answer/', views.accept_answer, name='accept-answer'),
    path('delete/<id>/', views.delete_faq, name='delete-faq'),
    path('report/<id>/', views.report_faq, name='report-faq'),
]