from django.contrib import admin
from .models import Post, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    model = Post
    filter_horizontal = ('tags','likes')
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
