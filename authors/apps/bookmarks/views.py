from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework import status

# local imports
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ArticleSerializer
from .models import BookmarkArticle
from .serializers import BookmarkSerializer


class BookmarkPaginator(PageNumberPagination):
    """
    Article paginator
    """
    page_size = 10
    page_size_query_param = 'page_size'


class BookmarkAPIView(CreateAPIView):
    """
    Views for bookmark functionality
    """
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)


    def post(self, request, art_slug=None, pk=None):
        """
        Create bookmark method
        """
        article = Article.objects.get(art_slug=art_slug)
        bookmark = {}
        bookmark['user'] = self.request.user.id
        bookmark['article'] = article.pk
        serializer = self.serializer_class(data=bookmark)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        article_serializer = ArticleSerializer(
            instance=article, context={'request': request})
        data = {"article": article_serializer.data}
        data["message"] = "bookmarked"

        return Response({
            "message": data.get('message'),
            }, status=status.HTTP_201_CREATED)

    def check_article(self, art_slug):
        """
        Check if article with the passed art_slug exists
        else return 404
        """
        try:
            article = Article.objects.get(art_slug=art_slug)
        except Article.DoesNotExist:
            raise NotFound(detail={'message': 'Article not found'})
        return article

    def check_bookmark(self, user, article):
        """
        Check if article is bookmarked already
        """
        try:
            bookmark = BookmarkArticle.objects.get(user=user, article=article.id)
        except BookmarkArticle.DoesNotExist:
            raise NotFound(detail={'message': 'This article has not been bookmarked'})

        return bookmark

    def delete(self, request, art_slug=None):
        """
        Method for deleting bookmarked article
        """
        user = self.request.user.id
        article = self.check_article(art_slug)
        bookmark = self.check_bookmark(user, article)

        if bookmark:
            bookmark.delete()
        article_serializer = ArticleSerializer(
            instance=article, context={'request': request}
            )
        data = article_serializer.data
        data['message'] = 'Successfully removed from bookmark'
        return Response(
            {'message': data.get('message')}
            )

class BookmarkRetrieveAPIView(RetrieveAPIView):
    """
    Views to retrieve all bookmarks by the current user
    """
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = BookmarkPaginator

    def get_queryset(self):
        user = self.request.user
        return user.bookmarkarticle_set.all().order_by('-created_at')

    def get(self, request, art_slug=None):
        """
        Method to retrieve all bookmarks by the current user
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({'articles':serializer.data}, status=status.HTTP_200_OK)
