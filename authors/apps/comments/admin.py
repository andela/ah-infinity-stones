from django.contrib import admin

# local imports
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    """
    Class defines fields to display on admin page
    """
    list_display = ('comment', 'thread', 'author')


admin.site.register(Comment, CommentAdmin)
