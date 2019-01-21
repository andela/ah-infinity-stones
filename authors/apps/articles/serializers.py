from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from django.apps import apps
from taggit_serializer.serializers import (TagListSerializerField)
from authors.apps.profiles.serializers import ProfileSerializer
Profile = apps.get_model('profiles', 'Profile')
from authors.apps.articles.models import (Article, User, Tag, Comment,
                                          LikeDislike, FavoriteArticle,
                                          ArticleRating, ArticleReporting)
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
    author = serializers.SerializerMethodField(read_only=True)
    tag = TagListSerializerField()
    share_urls = serializers.SerializerMethodField(read_only=True)
    favourite = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ("art_slug", "title", "description", "body", "read_time", "tag", 
                  "favourite", "likes_count", "dislikes_count", "liking", "disliking",
                  "rating_average", "share_urls", "author", "created_at", "updated_at")

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


class ArticleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleRating
        """
        Declare all fields we need to be returned from ArticleRating model
        """
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ArticleRatingSerializer, self).__init__(*args, **kwargs)

        # Override the error_messages of each field with a custom error message
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['null'] = field_error_messages['blank'] \
                = field_error_messages['required'] \
                = 'Please fill in the {}'.format(field)

    def update(self, instance, validated_data):
        """
        Method for updating an existing ArticleRating object
        """
        
        instance.art_slug = validated_data.get('art_slug', instance.art_slug)
        instance.username = validated_data.get('username', instance.username)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Method for creating an ArticleRating object
        It checks if a user has made a rating for an article. If yes it calls
        the update method. If not, it creates a new ArticleRating object.
        """
        article_rating_object, created = ArticleRating.objects.get_or_create(
            art_slug=validated_data.get('art_slug'),
            username=validated_data.get('username'),
            defaults={'rating': validated_data.get('rating', None)}, )
        
        if not created:
            self.update(instance=article_rating_object,
                        validated_data=validated_data)

        return article_rating_object


class ArticleReportingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleReporting
        """
        Declare all fields we need to be returned from ArticleReporting model
        """
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ArticleReportingSerializer, self).__init__(*args, **kwargs)

        # Override the error_messages of each field with a custom error message
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['null'] = field_error_messages['blank'] \
                = field_error_messages['required'] \
                = 'Please fill in the {}'.format(field)

    def update(self, instance, validated_data):
        """
        Method for updating an existing ArticleReporting object
        """
        
        instance.art_slug = validated_data.get('art_slug', instance.art_slug)
        instance.username = validated_data.get('username', instance.username)
        instance.report_msg = validated_data.get('report_msg',
                                                 instance.report_msg)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Method for creating an ArticleReporting object
        It checks if a user has reported an article. If yes it calls
        the update method. If not, it creates a new ArticleReporting object.
        """
        article_reporting_object, created = ArticleReporting.objects.get_or_create(
                        art_slug=validated_data.get('art_slug'),
                        username=validated_data.get('username'),
                        defaults={'report_msg': validated_data.get('report_msg', None)}, )
        
        if not created:
            self.update(instance=article_reporting_object,
                        validated_data=validated_data)

        return article_reporting_object


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
