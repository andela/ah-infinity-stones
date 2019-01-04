from django.urls import path, include

# local imports
from .views import (ArticleCommentAPIView, ArticleCommentUpdateDeleteAPIView, )
from .models import Comment

app_name = 'comments'

urlpatterns = [
    path('comments/', ArticleCommentAPIView.as_view(), name='comment'),
    path('comments/<int:id>/', ArticleCommentUpdateDeleteAPIView.as_view(), name='update_comment'),
]

