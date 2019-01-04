
from django.urls import path, include

from .views import LikeDislikeView
from authors.apps.likedislike.models import CommentLikeDislike as LikeDislike
from authors.apps.articles.models import Article
from authors.apps.comments.models import Comment

app_name = 'likedislike'

urlpatterns = [
    path('articles/<slug:art_slug>/like',
         LikeDislikeView.as_view(model=Article, vote_type=LikeDislike.LIKE),
         name='article_like'),
    path('articles/<slug:art_slug>/dislike',
         LikeDislikeView.as_view(model=Article, vote_type=LikeDislike.DISLIKE),
         name='article_dislike'),
    path('comments/<int:id>/like',
         LikeDislikeView.as_view(model=Comment, vote_type=LikeDislike.LIKE),
         name='comment_like'),
    path('comments/<int:id>/dislike',
         LikeDislikeView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE),
         name='comment_dislike'),
]
