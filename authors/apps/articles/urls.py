from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ArticleCreateView,
    DetailsView,
    ArticleListAPIView,
    CommentCreateViewAPIView,
    CommentListAPIView,
    CommentUpdateView,
    ArticleLikeDislikeView)


urlpatterns = [
    path('articles', ArticleCreateView.as_view(), name='articles'),
    path('articles/<art_slug>', DetailsView.as_view(), name='update'),
    path('articles', ArticleListAPIView.as_view(), name='list'),
    path(
        'articles/<art_slug>/like-dislike', ArticleLikeDislikeView.as_view(),
        name='like_article'),
    path('comment/', CommentCreateViewAPIView.as_view(), name='comment'),
    path('comment/', CommentListAPIView.as_view(), name='all_comments'),
    path(
        'comment/<slug>', CommentUpdateView.as_view(),
        name='update_comment'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
