from django.urls import path, re_path
from .views import (LoginView, RegistrationAPIView,
                    SocialAuthAPIView, ActivationView
                    )

urlpatterns = [
    path('users/', RegistrationAPIView.as_view(), name='register'),
    path('login/oauth/', SocialAuthAPIView.as_view(), name="social_auth"),
    path('users/login', LoginView.as_view(), name="login"),
    re_path(r'^user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+))/',
            ActivationView.as_view())
]
