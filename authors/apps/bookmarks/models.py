from django.db import models

# local imports
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class BookmarkArticle(models.Model):
    """
    Create the bookmark model
    """
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='bookmark_url', verbose_name='Article', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        unique_together = (('user', 'article'),)
        ordering = ['-created_at']

    def __str__(self):
        """
        Nice string of user and bookmarked article
        """
        return "{} bookmarked by user {}".format(self.article, self.user)
