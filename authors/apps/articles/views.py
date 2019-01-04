import math

from authors.apps.articles.models import (Article, Comment, LikeDislike,
                                          ArticleRating, FavoriteArticle,
                                          ArticleReporting)
from rest_framework import generics
from .serializers import (ArticleSerializer, CommentSerializer, LikeSerializer,
                          ArticleRatingSerializer, FavoriteSerializer,
                          ArticleReportingSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListAPIView,)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from django.core.exceptions import ObjectDoesNotExist
import json
from django.db.models import Avg
from django.core import serializers
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string


class ArticleCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """ Method for creating an article """
        article = serializer.save(user=self.request.user)
        tags = Article.objects.get(pk=article.pk)
        for tag in article.tag:
            tags.tag.add(tag)
        text = serializer.validated_data['body']
        read_time = self.article_read_time(text)
        serializer.save(user=self.request.user, read_time=read_time)
        return Response({
            "Message": "article created successfully",
            "Data": serializer.data
        },
                        status=status.HTTP_201_CREATED)

    def article_read_time(self, text):
        """Method that calculates article read time"""
        wpm = 200
        total_words = len(text.split())
        read_time = total_words / wpm
        return int(math.ceil(read_time))


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'art_slug'

    def put(self, request, art_slug, *args, **kwargs):
        """ Method for updating an article """
        try:
            article = Article.objects.get(art_slug=art_slug)
            serializer_data = request.data

            if 'body' in request.data:
                text = serializer_data['body']
                pc = ArticleCreateView
                read_time = pc.article_read_time(self, text)
                serializer_data['read_time'] = read_time

            serializer = self.serializer_class(
                article, data=serializer_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "article updated successfully",
                "Articles": serializer.data
            },
                            status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({
                "message": "Article does not exist"
            },
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, art_slug):
        """ Method for deleting an article """
        try:
            queryset = Article.objects.get(art_slug=art_slug)
            queryset.delete()
            return Response({
                "message": "article deleted successfully"
            },
                            status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response({
                "message": "Article does not exist"
            },
                            status=status.HTTP_404_NOT_FOUND)


class SearchArticleView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ArticleSerializer

    def get(self, request):
        search_params = request.query_params
        query_set = Article.objects.all()

        author = search_params.get('author', "")
        title = search_params.get('title', "")
        tag = search_params.get('tag', "")
        keywords = search_params.get('q', "")
        # filter based on the specific filter
        if author:
            query_set = query_set.filter(user__username=author)
        elif title:
            query_set = query_set.filter(title=title)
        elif tag:
            query_set = query_set.filter(tag__name=tag)
        elif keywords:
            # split the list of comma separated keywords
            words = str(keywords).split(',')
            final_queryset = ''
            for word in words:
                # filter titles based on the keyword(s) passed and
                # append them to final_queryset
                final_queryset = query_set.filter(title__icontains=word)
            query_set = final_queryset

        serializer = self.serializer_class(query_set, many=True)
        return_data = serializer.data
        if len(return_data) > 0:
            return Response({"Your search results": return_data},
                            status.HTTP_200_OK
                            )
        return Response({"Message": "Your search query did not match"
                         " anything in the database"})


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, slug):
        """ Method for getting all articles """
        return Response(status=status.HTTP_200_OK)

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleRatingAPIView(generics.ListCreateAPIView):
    """
    Create a new article rating
    """
    permission_classes = (IsAuthenticated,)
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleRatingSerializer

    def get(self, request, art_slug):
        """
        Audience can see all ratings for an article
        """
        try:
            article_ratings = ArticleRating.objects.filter(art_slug=art_slug)
            article_ratings_data = serializers.serialize("json",
                                                         article_ratings,
                                                         fields=('username',
                                                                 'rating'))
            article_ratings_json = json.loads(article_ratings_data)
            all_ratings = []
            for i in range(len(article_ratings_json)):
                all_ratings.append(article_ratings_json[i]['fields']) 
        except Exception:
            response = {"message": "That article does not exist"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        return Response(all_ratings, status=status.HTTP_200_OK)

    def post(self, request, art_slug):
        """
        Audience can post a rating for an article
        """
        # Retrieve article rating data from the request object and convert it
        # to a kwargs object
        # get user data at this point
        try:
            article = Article.objects.get(art_slug=art_slug)
        except Exception:
            response = {"message": "That article does not exist"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article.user_id == request.user.id:
            data = {
                "message": "You cannot rate your own article."
            }
            return Response(data, status.HTTP_403_FORBIDDEN)

        article_rating = {
            'art_slug': art_slug,
            'username': request.user.username,
            'rating': request.data.get('rating', None),
        }
        # pass article data to the serializer class, check whether the data is
        # valid and if valid, save it.
        serializer = self.serializer_class(data=article_rating)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Save the average article rating to the Article model
        q = ArticleRating.objects.filter(art_slug=article.art_slug).aggregate(
            Avg('rating'))
        article.rating_average = q['rating__avg']
        article.save(update_fields=['rating_average'])
        data = {"message": "Thank you for taking time to rate this article."}

        return Response(data, status.HTTP_201_CREATED)


class ArticleReportingAPIView(generics.ListCreateAPIView):
    """
    Report an article
    """
    permission_classes = (IsAuthenticated,)
    queryset = ArticleRating.objects.all()
    serializer_class = ArticleReportingSerializer

    def post(self, request, art_slug):
        """
        Audience can report an article
        """
        # Retrieve article rating data from the request object and convert it
        # to a kwargs object
        # get user data at this point
        try:
            article = Article.objects.get(art_slug=art_slug)
        except Exception:
            response = {"message": "That article does not exist"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if article.user_id == request.user.id:
            data = {
                "message": "You cannot report your own article."
            }
            return Response(data, status.HTTP_403_FORBIDDEN)

        article_reporting = {
            'art_slug': art_slug,
            'username': request.user.username,
            'report_msg': request.data.get('report_msg', None),
        }
        # pass article reporting data to the serializer class, check whether
        # the data is valid and if valid, save it.
        serializer = self.serializer_class(data=article_reporting)
        serializer.is_valid(raise_exception=True)
        domain = '127.0.0.1:8000'
        time = datetime.now()
        time = datetime.strftime(time, '%d-%B-%Y %H:%M')
        message = render_to_string('report_article.html', {
            'user': 'Admin',
            'admin': 'Admin',
            'username': request.user.username,
            'art_slug': art_slug,
            'report_msg': request.data.get('report_msg', None),
            'time': time,
            'link': 'http://' + domain + '/api/articles/' +
                    art_slug})
        mail_subject = 'Article:'+art_slug+' has been reported.'
        to_email = 'ronnymageh@gmail.com'
        from_email = 'infinitystones.team@gmail.com'
        send_mail(
            mail_subject,
            'Article:'+art_slug+' reported.',
            from_email,
            [to_email, ],
            html_message=message, fail_silently=False)

        serializer.save()
        data = {"message": "You have reported this article to the admin."}

        return Response(data, status.HTTP_201_CREATED)


class CommentCreateViewAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)


class ArticleLikeDislikeView(generics.ListCreateAPIView):
    """ Like/Dislike article class view"""
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, art_slug):
        """
        Implement article like or a dislike
        """
        like = request.data.get('like', None)
        like = like.capitalize()
        if like is None or not isinstance(bool(like), bool):
            return Response({
                'Message': "Like can only be True or False"
            }, status.HTTP_400_BAD_REQUEST)
        liked = None
        try:
            article = Article.objects.get(art_slug=art_slug)
        except ObjectDoesNotExist:
            return Response({
                'Message': 'The article does not exist'
            }, status.HTTP_404_NOT_FOUND)
        # has the user already liked this article?
        try:
            liked = LikeDislike.objects.get(
                user=request.user.id, article=article)
        except ObjectDoesNotExist:
            # in case the user hasn't liked dont break or bring error
            pass
        if liked:
            # user can now switch from liking to disliking
            if liked.like is True and like != 'True':
                liked.like = like
                liked.save()
                return Response({
                    "Message": "You disliked this article"
                }, status.HTTP_200_OK)
            elif liked.like is not True and like == 'True':
                liked.like = like
                liked.save()
                return Response({
                    "Message": "You liked this article"
                }, status.HTTP_200_OK)
            elif liked.like is True and like == 'True':
                # A user can only like once
                liked.delete()
                msg = '{}, you have unliked this article.'.format(
                    request.user.username)
                return Response({'Message': msg}, status.HTTP_204_NO_CONTENT)
            elif liked.like is not True and like != 'True':
                liked.delete()
                msg = '{}, you have undisliked this article.'.format(
                    request.user.username)
                return Response({'Message': msg}, status.HTTP_204_NO_CONTENT)
        else:
            new_like = {
                'article': article.id,
                'user': request.user.id,
                'like': like
            }
            serializer = self.serializer_class(data=new_like)
            serializer.is_valid(raise_exception=True)
            serializer.save(article=article, user=request.user)
        return Response({
            'Message':
            ("Thank you {} for your opinion ".format(request.user.username))
        }, status.HTTP_201_CREATED)


class FavouriteArticleAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    """Incase the user feels satisfied with the article, he can favourite it
    and incase he feels disatisfied with the article he can Unfavourite it. """

    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )

    def article_exists(self, art_slug):
        try:
            article = Article.objects.get(art_slug=art_slug)
        except Article.DoesNotExist:
            return Response({
                'Message': 'The article does not exist'
            }, status.HTTP_404_NOT_FOUND)
        return article

    def post(self, request, art_slug):
        """
       Implement article favorite  or unfavorite
       """

        article = self.article_exists(art_slug)

        favorited = FavoriteArticle.objects.filter(
            user=request.user.id, article=article.id).exists()

        if favorited:
            return Response(
                {
                    'Message': "You have already favourited this article"
                }, status.HTTP_400_BAD_REQUEST)

        data = {"article": article.id, "user": request.user.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "Message": "You have successfully favorited this article."
            }, status.HTTP_200_OK)

    def delete(self, request, art_slug):
        """
       Implement article favorite  or unfavorite
       """

        article = self.article_exists(art_slug)

        favorited = FavoriteArticle.objects.filter(
            user=request.user.id, article=article.id).exists()

        if not favorited:
            return Response(
                {
                    'Message': "You have already unfavourited this article"
                }, status.HTTP_400_BAD_REQUEST)

        instance = FavoriteArticle.objects.filter(
            user=request.user.id, article=article.id)

        self.perform_destroy(instance)

        return Response(
            {
                "Message": "You have successfully unfavorited this article."
            }, status.HTTP_200_OK)
