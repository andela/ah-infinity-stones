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
    path(
        'user/activate/<uidb64>/<token>',
        ActivationView.as_view(),
        name='activate'),
]
