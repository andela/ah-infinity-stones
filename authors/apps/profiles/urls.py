from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.ProfileApiView.as_view(), name='profile'),
    path('u', views.ProfileRetrieve.as_view(), name='currentprofile'),
    path('<username>', views.ProfileRetrieveUpdate.as_view(), name='userprofile'),
]