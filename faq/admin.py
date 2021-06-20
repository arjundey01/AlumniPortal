from django.contrib import admin
from .models import Question, Answer
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    filter_horizontal = ('tags', 'likes')

admin.site.register(Question)
admin.site.register(Answer)
