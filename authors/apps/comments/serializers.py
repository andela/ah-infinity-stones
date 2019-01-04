from rest_framework import serializers

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'article',
            'thread',
            'comment',
            'author'
             )

        extra_kwargs = {
            # Works ok with put but buggy with post
        }

