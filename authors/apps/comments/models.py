from django.db import models

# local imports
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField


class Comment(models.Model):
    """Models comment"""
    comment = models.CharField(max_length=255, null=False)
    # Use self to denote comment is thread if first
    thread = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='thread_1')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_1', default=1)
    author = models.ForeignKey(User, related_name='comment_1', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Surfer(models.Model):
    """Models current user"""
    surfer = CurrentUserField()

    def __str__(self):
        return str(self.surfer)
