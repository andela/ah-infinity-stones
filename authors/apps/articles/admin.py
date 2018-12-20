from django.contrib import admin

# local imports
from .models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    """
    Class defines fields to display on admin page
    """
    list_display = ('title', 'description', 'read_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
