from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from authors.apps.authentication.serializers import UserSerializer
import json


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            'user',
<<<<<<< HEAD
            'firstname',
            'lastname',
            'birthday',
            'image',
            'bio'
=======
            'bio',
            'birthday',
            'gender',
            # 'image',
>>>>>>> ce71ac7... [FEATURE #161966915] setup userprofiles app
        )

        extra_kwargs = {
            'user': {'read_only': True}
        }

