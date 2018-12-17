from django.urls import path, re_path
from .views import (LoginAPIView, RegistrationAPIView, SocialAuthAPIView,
                    ActivationView, PasswordResetBymailAPIView,
                    PasswordResetDoneAPIView)

urlpatterns = [
    path('users/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('login/oauth/', SocialAuthAPIView.as_view(), name="social_auth"),
    path(
        'user/password-reset/',
        PasswordResetBymailAPIView.as_view(),
        name='reset'),
    path(
        'users/reset/<str:token>',
        PasswordResetDoneAPIView.as_view(),
        name='update_password'),
    re_path(
        r'^user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/\
    (?P<token>[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+))/',
        ActivationView.as_view(),
        name='activate'),
]
