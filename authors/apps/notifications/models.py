from django.db import models
from ..authentication.models import User
from ..articles.models import Article

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
