from authors.apps.articles.models import (Article, Comment, LikeDislike)
from rest_framework import generics
from .serializers import (ArticleSerializer, CommentSerializer, LikeSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListAPIView,)
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist


class ArticleCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """ Method for creating an article """
        serializer.save(user=self.request.user)
        return Response({"Message": "article created successfully", "Data":
                         serializer.data}, status=status.HTTP_201_CREATED)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'art_slug'

    def put(self, request, art_slug, *args, **kwargs):
        """ Method for updating an article """
        try:
            article = Article.objects.get(art_slug=art_slug)
            serializer_data = request.data
            serializer = self.serializer_class(
                article, data=serializer_data, partial=True)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({"message": "article updated successfully",
                             "Articles": serializer.data},
                            status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({"message": "Article does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, art_slug):
        """ Method for deleting an article """
        try:
            queryset = Article.objects.get(art_slug=art_slug)
            queryset.delete()
            return Response({"message": "article deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response({"message": "Article does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, slug):
        """ Method for getting all articles """
        return Response(status=status.HTTP_200_OK)


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
            return Response(
                {'Message': "Like can only be True or False"},
                status.HTTP_400_BAD_REQUEST)
        liked = None
        try:
            article = Article.objects.get(art_slug=art_slug)
        except ObjectDoesNotExist:
            return Response(
                {
                    'Message': 'The article does not exist'
                }, status.HTTP_404_NOT_FOUND
            )
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
                return Response(
                    {"Message": "You disliked this article"},
                    status.HTTP_200_OK)
            elif liked.like is not True and like == 'True':
                liked.like = like
                liked.save()
                return Response(
                    {"Message": "You liked this article"}, status.HTTP_200_OK)
            elif liked.like is True and like == 'True':
                # A user can only like once
                liked.delete()
                msg = '{}, you have unliked this article.'.format(
                    request.user.username)
                return Response(
                    {
                        'Message': msg
                    }, status.HTTP_204_NO_CONTENT
                )
            elif liked.like is not True and like != 'True':
                liked.delete()
                msg = '{}, you have undisliked this article.'.format(
                    request.user.username)
                return Response(
                    {
                        'Message': msg
                    }, status.HTTP_204_NO_CONTENT
                )
        else:
            new_like = {
                'article': article.id,
                'user': request.user.id,
                'like': like
            }
            serializer = self.serializer_class(data=new_like)
            serializer.is_valid(raise_exception=True)
            serializer.save(article=article, user=request.user)
        return Response(
            {'Message': ("Thank you {} for your opinion ".format(
                request.user.username)
            )
            }, status.HTTP_201_CREATED
        )
