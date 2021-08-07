from django.contrib import admin
from .models import PostCategory, Post, Comment


admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Comment)

