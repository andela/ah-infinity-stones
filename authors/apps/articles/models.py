from django.db import models
from authors.apps.authentication.models import (
    User
)


class Tag(models.Model):
    """This class represents the Tag model"""
    tag = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.tag)


class Article(models.Model):
    """This class represents the Articles model"""
    title = models.CharField(max_length=50, null=False, unique=True)
    author = models.ManyToManyField(User)
    tag = models.ManyToManyField(Tag)
    description = models.CharField(max_length=250, null=False, default="")
    body = models.TextField(null=False, default="")
    read_time = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.title)


class FavoriteArticle(models.Model):
    """This class represents the Favorite Articles model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    favorite = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.favorite)


class Comment(models.Model):
    """This class represents the Favorite Comment model"""
    # article = models.ManyToManyField(Article)
    article = models.ForeignKey(Article, related_name='commento', null=True, blank=True, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, related_name='commento', blank=True, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.comment)


class CommentHistory(models.Model):
    """This class represents the Comment History model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    comment = models.ManyToManyField(Comment)
    new_comment = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.new_comment)


class LikesDislike(models.Model):
    """This class represents the Favorite Likes Dislike model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.like)


class ArticleRating(models.Model):
    """This class represents the Favorite Article Rating model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    rating = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.rating)


class BookmarkedArticle(models.Model):
    """This class represents the Favorite Article Rating model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    bookmarked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.bookmarked)


class Report(models.Model):
    """This class represents the Reports model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    message = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.message)


class Highlight(models.Model):
    """This class represents the Highlight model"""
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
    section = models.TextField(null=False)
    index_start = models.IntegerField(default=0)
    index_end = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.section)
