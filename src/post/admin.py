from django.contrib import admin

from .models import Article, Like


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'body', 'author')


admin.site.register(Like)
