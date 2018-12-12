"""
Imports
"""
from django.contrib import admin

from .models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    """
    Class to define fields to display on admin page
    """
    list_display = ('title', 'description', 'body', 'read_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
