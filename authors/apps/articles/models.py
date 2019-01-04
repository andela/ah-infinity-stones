import uuid
from django.db import models
from taggit.managers import TaggableManager
from authors.apps.authentication.models import (User)
from django.utils.text import slugify
from rest_framework.reverse import reverse as api_reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from authors.apps.likedislike.models import CommentLikeDislike as LikeDislike

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
    rating_average = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)
    read_time = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(LikeDislike, related_query_name='articles')

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
        self.art_slug = self.generate_slug()
        super(Article, self).save(*args, **kwargs)

    def get_share_uri(self, request=None):
        """
        This method allow users to share articles on Twitter, Facebook,
         and Email.
        """
        article_share_url = "https://ah-infinites-staging.herokuapp.com/api/articles/{}".format(
            self.art_slug
        )

        url_content = {
            "twitter":
                "https://twitter.com/intent/tweet?url = {}".format(
                    article_share_url),
            "facebook":
                "https://www.facebook.com/sharer/sharer.php?u = {}".format(
                    article_share_url),
            "email":
                "mailto:?subject = New Article Alert&body = {}".format(
                    article_share_url)
        }
        return url_content


class FavoriteArticle(models.Model):
    """This class represents the Favorite Articles model"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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


class LikeDislike(models.Model):
    """ Like and dislike data model"""
    class Meta:
        # user can only like article once
        unique_together = (('article', 'user'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ArticleRating(models.Model):
    """This class represents the Article Rating model"""
    art_slug = models.ForeignKey(Article, to_field="art_slug",
                                 db_column="art_slug",
                                 on_delete=models.CASCADE)
    username = models.ForeignKey(User, to_field="username",
                                 db_column="username",
                                 on_delete=models.CASCADE)
    # rating is from 1 to 5
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                 MaxValueValidator(5)])
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


class ArticleReporting(models.Model):
    """This class represents the Article Reporting model"""
    art_slug = models.ForeignKey(Article, to_field="art_slug",
                                 db_column="art_slug",
                                 on_delete=models.CASCADE)
    username = models.ForeignKey(User, to_field="username",
                                 db_column="username",
                                 on_delete=models.CASCADE)
    report_msg = models.CharField(null=False, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a human readable representation of the model instance"""
        return "{}".format(self.report_msg)


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
