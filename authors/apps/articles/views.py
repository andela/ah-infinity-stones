from authors.apps.articles.models import Article, Comment, FavoriteArticle
from rest_framework import generics
from .serializers import (ArticleSerializer, CommentSerializer,
                          FavoriteSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated


class ArticleCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({"message": "article created successfully"},status = status.HTTP_201_CREATED)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'art_slug'

    def update(self, request, art_slug, *args, **kwargs):
        article = Article.objects.get(art_slug=art_slug)
        serializer_data = request.data
        serializer = self.serializer_class(
            article, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "article updated successfully", "Data":
                         serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, art_slug):
        queryset = Article.objects.get(art_slug=art_slug)
        queryset.delete()
        return Response({"message": "article deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, slug):
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