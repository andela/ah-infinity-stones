from django.urls import path

# local imports
from .views import BookmarkAPIView, BookmarkRetrieveAPIView

app_name = 'bookmarks'

urlpatterns = [
    path('articles/<slug:art_slug>/bookmark', BookmarkAPIView.as_view(), name='bookmarks'),
    path('bookmarks/', BookmarkRetrieveAPIView.as_view(), name='all_bookmarks'),
]
