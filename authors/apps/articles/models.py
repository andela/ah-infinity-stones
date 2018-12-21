import uuid

from django.db import models
from taggit.managers import TaggableManager
from authors.apps.authentication.models import (User)
from django.utils.text import slugify


class Tag(models.Model):
    """This class represents the Tag model"""
    tag = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.tag)


class Article(models.Model):
    """This class represents the Articles model"""
    art_slug = models.SlugField(
        db_index=True, max_length=250, unique=True, blank=True)
    title = models.CharField(max_length=250, null=False)
    user = models.ForeignKey(
        User, related_name='articles', on_delete=models.CASCADE)
    tag = TaggableManager(blank=True)
    description = models.CharField(max_length=250, null=False, default="")
    body = models.TextField(null=False)
    read_time = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.title)

    def generate_slug(self):
        """
       Generate a unique identifier for each article.
        """
        slug = slugify(self.title)
        while Article.objects.filter(art_slug=slug).exists():
            slug = slug + '-' + uuid.uuid4().hex
        return slug

    def save(self, *args, **kwargs):
        """
        Add generated slug to save function.
        """
        if not self.art_slug:
            self.art_slug = self.generate_slug()
        super(Article, self).save(*args, **kwargs)


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
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(User)
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
    author = models.ManyToManyField(User)
    section = models.TextField(null=False)
    index_start = models.IntegerField(default=0)
    index_end = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.section)
