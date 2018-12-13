from django.urls import path, re_path

from .views import LoginAPIView, RegistrationAPIView, \
    UserRetrieveUpdateAPIView, SocialAuthAPIView, ActivationView

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('login/oauth/', SocialAuthAPIView.as_view(), name="social_auth"),
    re_path(r'^user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+))/',
            ActivationView.as_view()),
    path('socialAuth/', SocialAuthAPIView.as_view()),
]
