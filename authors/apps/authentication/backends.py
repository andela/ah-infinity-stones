import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    """This class implement the JWT token"""

    def authenticate(self, request):
        """This method validates user token and returns the token along with\
         the user"""
        token = authentication.get_authorization_header(request)
        # Check whether a token is returned
        if not token:
            return None
        # Try to decode the token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        except:
            raise AuthenticationFailed("Your token is invalid")
        # Get user credentials for the user owing the token
        try:
            user = User.objects.get(email=payload["email"])
        except User.DoesNotExist:
            raise AuthenticationFailed('No user found for token provided')

        # Check whether the user is active
        if not user.is_active:
            raise AuthenticationFailed("Your account is disabled, please visit your account to activate")
        return (user, token)

    def generate_token(self, email):
        """
        Generate and return a decoded token.
        """
        date_time = datetime.now() + timedelta(days=2)

        payload = {
            'email': email,
            'exp': int(date_time .strftime('%s'))
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
