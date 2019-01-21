from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ArticleCreateView,
    DetailsView,
    ArticleListAPIView,
    CommentCreateViewAPIView,
    CommentListAPIView,
    CommentUpdateView,
    ArticleLikeDislikeView,
    ArticleRatingAPIView,
    SearchArticleView,
    ArticleReportingAPIView,
    FavouriteArticleAPIView)


urlpatterns = [
    path('articles', ArticleCreateView.as_view(), name='articles'),
    path('articles/<art_slug>', DetailsView.as_view(), name='update'),
    path('articles', ArticleListAPIView.as_view(), name='list'),
    path(
        'articles/<art_slug>/like-dislike',
        ArticleLikeDislikeView.as_view(),
        name='like_article'),
    path('articles/search/', SearchArticleView.as_view(), name='search'),
    path('comment/', CommentCreateViewAPIView.as_view(), name='comment'),
    path('comment/', CommentListAPIView.as_view(), name='all_comments'),
    path('comment/<slug>', CommentUpdateView.as_view(), name='update_comment'),
    path(
        'articles/<art_slug>/favourite',
        FavouriteArticleAPIView.as_view(),
        name='favourite_article'),
    path('articles/<art_slug>/rate', ArticleRatingAPIView.as_view(),
         name='rate'),
    path('articles/<art_slug>/report', ArticleReportingAPIView.as_view(),
         name='report'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
