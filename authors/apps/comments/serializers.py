from rest_framework import serializers

from .models import Comment
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.articles.models import Article
from authors.apps.comments.models import Comment
from authors.apps.profiles.models import Profile

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment 
        fields = (
            'id',
            'article',
            'thread',
            'comment',
            'author',
            'created_at',
            'updated_at'
             )

        extra_kwargs = {
            # Works ok with put but buggy with post
        }

    def get_author(self, obj):

            try:
                serializer = ProfileSerializer(
                    instance=Profile.objects.get(user=obj.author)
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

