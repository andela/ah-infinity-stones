from rest_framework import authentication
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    This is called on every request to check if the user is authenticated
    """

    def authenticate(self, request):
       pass
