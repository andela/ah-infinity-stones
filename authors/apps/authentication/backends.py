from rest_framework import authentication


class JWTAuthentication(authentication.BaseAuthentication):
    """JWT config"""

    def authenticate(self, request):
        pass
