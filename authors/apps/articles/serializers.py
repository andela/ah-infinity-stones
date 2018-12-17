from rest_framework import serializers
from django.apps import apps
from taggit_serializer.serializers import (TagListSerializerField)
from authors.apps.profiles.serializers import ProfileSerializer
Profile = apps.get_model('profiles', 'Profile')
from authors.apps.articles.models import (
    Article, User, Tag, Comment, LikeDislike)
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


class LikeSerializer(serializers.ModelSerializer):
    """ Serialize json to model and model to json"""

    class Meta:
        model = LikeDislike
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=LikeDislike.objects.all(),
                fields=('article', 'user')
            )
        ]
