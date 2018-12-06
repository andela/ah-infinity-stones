from django.db import models
from ..authentication.models import User


class Article(models.Model):
    """This class creates the Article model"""
    title = models.CharField(max_length=50, null=False, unique=True)
    author = models.ManyToManyField(User)
    description = models.CharField(max_length=250, null=False, default="")
    body = models.TextField(null=False, default="")
    read_time = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.title)


class Notification(models.Model):
    """This class creates the Notification model"""
    article = models.ManyToManyField(Article)
    title = models.CharField(max_length=150, blank=False)
    body = models.TextField()
    user = models.ManyToManyField(User)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=150, default="article")
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        "Returns a string representation of notification model."
        return "{}".format(self.title)
