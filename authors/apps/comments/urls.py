from django.urls import path, include

# local imports
from .views import (ArticleCommentAPIView, ArticleCommentUpdateDeleteAPIView, )
from .models import Comment

app_name = 'comments'

urlpatterns = [
    path('comments/<slug:art_slug>/', ArticleCommentAPIView.as_view(), name='comment'),
    path('comments/<slug:art_slug>/all', ArticleCommentAPIView.as_view(), name='comment_all'),
    path('comments/<slug:art_slug>/<int:id>/', ArticleCommentUpdateDeleteAPIView.as_view(), name='update_comment'),
]

