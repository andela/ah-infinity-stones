from django.urls import path, include

# local imports
from .views import (ArticleCommentAPIView, ArticleCommentUpdateDeleteAPIView, )
from .models import Comment

app_name = 'comments'

urlpatterns = [
    path('articles/<slug:art_slug>/comments/', ArticleCommentAPIView.as_view(), name='comment'),
    path('articles/<slug:art_slug>/comments/all', ArticleCommentAPIView.as_view(), name='comment_all'),
    path('articles/<slug:art_slug>/comments/<int:id>/', ArticleCommentUpdateDeleteAPIView.as_view(), name='update_comment'),
]

