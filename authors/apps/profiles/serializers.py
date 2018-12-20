from rest_framework import serializers
from django.core.serializers import serialize
from django.contrib.auth import get_user_model

# local imports
from .models import Profile
from authors.apps.authentication.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            'user',
            'firstname',
            'lastname',
            'birthday',
            'image',
            'gender',
            'bio',
            'followers'
        )

        extra_kwargs = {
            'user': {'read_only': True}
        }

