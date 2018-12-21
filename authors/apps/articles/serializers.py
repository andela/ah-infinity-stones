from rest_framework import serializers
from authors.apps.articles.models import (Article, User, Tag, Comment,
                                          FavoriteArticle)
from taggit_serializer.serializers import (TagListSerializerField)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tag = TagListSerializerField()

    class Meta:

        model = Article
        fields =("id", "art_slug", "title", "description", "body", "read_time",
                  "tag", "user", "created_at", "updated_at")


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]


class FavoriteSerializer(serializers.ModelSerializer):
    """ Serialize json to model and model to json"""

    class Meta:
        model = FavoriteArticle
        fields = ('article', 'user')

    def create(self, validated_data):
        return FavoriteArticle.objects.create(**validated_data)
