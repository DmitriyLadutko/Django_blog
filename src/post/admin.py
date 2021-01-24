from django.contrib import admin

from .models import Article, Like, Category, Profile


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'body', 'author', 'year')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'bio', 'id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Like)
admin.site.register(Category)
