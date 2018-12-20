from django.urls import path
from .views import (ArticleCreateView, ArticleUpdateView, ArticleListAPIView,
                    ArticleDeleteAPIView, CommentCreateViewAPIView,
                    CommentListAPIView, CommentUpdateView)


urlpatterns = [
    path('articles', ArticleCreateView.as_view(), name='articles'),
    path('articles/<int:pk>', ArticleUpdateView.as_view(), name='update'),
    path('articles', ArticleListAPIView.as_view(), name='list'),
    path('delete/<int:pk>/', ArticleDeleteAPIView.as_view(), name='delete'),
    path('comment', CommentCreateViewAPIView.as_view(), name='comment'),
    path('comment', CommentListAPIView.as_view(), name='all_comments'),
    path(
        'comment/<int:pk>', CommentUpdateView.as_view(),
        name='update_comment'),
]
