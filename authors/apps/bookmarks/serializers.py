from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# local imports
from .models import BookmarkArticle

class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmark serialization
    """
    article_slug = serializers.ReadOnlyField(source='article.art_slug')
    article_title = serializers.ReadOnlyField(source='article.title')
    article_author = serializers.ReadOnlyField(source='article.user.username')

    class Meta:
        model = BookmarkArticle
        fields = ("id", "user", "article", "article_slug", "article_title", "article_author", "created_at")
        validators = [
            UniqueTogetherValidator(
                queryset=BookmarkArticle.objects.all(),
                fields=('article', 'user'),
                message='Sorry, you already bookmarked this article'
                )]
