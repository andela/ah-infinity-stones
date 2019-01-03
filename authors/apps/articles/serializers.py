from rest_framework import serializers
from django.apps import apps
from taggit_serializer.serializers import (TagListSerializerField)
from authors.apps.profiles.serializers import ProfileSerializer
Profile = apps.get_model('profiles', 'Profile')
from authors.apps.articles.models import (Article, User, Tag, Comment,
                                          LikeDislike, FavoriteArticle)
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer that converts querysets to json data"""
    user = serializers.ReadOnlyField(source='user.username')
    tag = TagListSerializerField()
    share_urls = serializers.SerializerMethodField(read_only=True)
    favourite = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ("art_slug", "title", "description", "body", "favourite",
                  "read_time", "tag", "user", "share_urls", "created_at",
                  "updated_at")

    def get_share_urls(self, instance):
        """
        Populates share_urls with google, facebook, and twitter share urls.
        """
        request = self.context.get('request')
        return instance.get_share_uri(request=request)

    def get_favourite(self, request):
        user = request.user_id
        article_id = request.id
        favorited = FavoriteArticle.objects.filter(
            user=user, article=article_id).exists()
        return favorited


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]


class LikeSerializer(serializers.ModelSerializer):
    """ Serialize json to model and model to json"""

    class Meta:
        model = LikeDislike
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=LikeDislike.objects.all(), fields=('article', 'user'))
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    """ Serialize json to model and model to json"""

    class Meta:
        model = FavoriteArticle
        fields = ('article', 'user')

    def create(self, validated_data):
        return FavoriteArticle.objects.create(**validated_data)
