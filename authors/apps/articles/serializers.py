from rest_framework import serializers
from django.apps import apps
from authors.apps.articles.models import Article, User, Tag, Comment
from taggit_serializer.serializers import (TagListSerializerField)
from authors.apps.profiles.serializers import ProfileSerializer

Profile = apps.get_model('profiles', 'Profile')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer that converts querysets to json data"""
    tag = TagListSerializerField()
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ("art_slug", "title", "description", "body", "read_time",
                  "tag",  "created_at", "updated_at", "author")

    def get_author(self, obj):

        try:
            serializer = ProfileSerializer(
                instance=Profile.objects.get(user=obj.user)
            )

            data = {
                "username": serializer.data['user']['username'],
                "bio": serializer.data['bio'],
                "image": serializer.data['image'],
                "following": ''
            }
            return data
        except Profile.DoesNotExist:
            return {"message": "User not found"}


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["article", "user", "comment"]
