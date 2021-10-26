from django.contrib import admin
from .models import PostCategory, Post, Comment, Author, Category


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating.short_description = 'Обнулить рейтинг статьи'


class PostAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_display = ['title', 'caregoryType', 'dateCreation', 'rating', 'rating_100']
    list_filter = ['caregoryType', 'dateCreation', 'rating', 'postCategory__name']
    search_fields = ['title', 'postCategory__name']
    actions = [nullfy_rating]


admin.site.register(PostCategory)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
