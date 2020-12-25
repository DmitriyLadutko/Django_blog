from django.contrib import admin

from .models import Article, Like, Category


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'body', 'author', 'year')


admin.site.register(Like)
admin.site.register(Category)
