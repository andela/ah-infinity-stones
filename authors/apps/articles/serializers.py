from rest_framework import serializers
from authors.apps.articles.models import Article, User, Tag, Comment
<<<<<<< HEAD
from taggit_serializer.serializers import (TagListSerializerField)
=======
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
>>>>>>> create an article and retrieve a specific article by id


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    """Article serializer that converts querysets to json data"""
=======
>>>>>>> create an article and retrieve a specific article by id
    user = serializers.ReadOnlyField(source='user.username')
    tag = TagListSerializerField()

    class Meta:

        model = Article
<<<<<<< HEAD
        fields = ("art_slug", "title", "description", "body", "read_time",
                  "tag", "user", "created_at", "updated_at")
=======
        fields = ("title", "description", "body", "read_time", "user", "tag",)
>>>>>>> create an article and retrieve a specific article by id


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]
