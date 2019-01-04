from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from . import views

router = routers.DefaultRouter()
app_name = 'profiles'

urlpatterns = [
    path('profiles/', views.ProfileApiView.as_view(), name='profile'),
    path('profiles/u', views.ProfileRetrieve.as_view(), name='currentprofile'),
    path('profiles/me', views.ProfileRetrieve.as_view(), name='currentprofile2'),
    path('profiles/<email>', views.ProfileRetrieveUpdate.as_view(), name='userprofile'),
]
