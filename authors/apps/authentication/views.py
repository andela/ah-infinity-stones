import jwt
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,\
 IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .backends import JWTAuthentication
from django.http import JsonResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from .models import User


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # jwt_auth = JWTAuthentication()
        """
        Generate and return a decoded token.
        """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        date_time = datetime.now() + timedelta(days=2)
        payload = {
            'email': user['email'],
            'exp': int(date_time .strftime('%s'))
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        token = token.decode('utf-8')
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        # email = user['email']
        # token = jwt_auth.generate_token(email)
        domain = '127.0.0.1:8000'
        self.uid = urlsafe_base64_encode(force_bytes(user['username'])).decode("utf-8")
        # token = user.token()
        # jwt_auth = JWTAuthentication()
        # token = jwt_auth.generate_token(user['email'])
        time = datetime.now()
        time = datetime.strftime(time, '%d-%B-%Y %H:%M')
        message = render_to_string('email_confirm.html', {
            'user': user,
            'domain': domain,
            'uid': self.uid,
            'token': token,
            'username': user['username'],
            'time': time,
            'link': 'http://' + domain + '/api/user/activate/' +
                    self.uid + '/' + token + '/'})
        mail_subject = 'Activate your account.'
        to_email = user['email']
        from_email = 'infinitystones.team@gmail.com'
        send_mail(
            mail_subject,
            'Verify your Account',
            from_email,
            [to_email, ],
            html_message=message, fail_silently=False)

        message = {'Message': '{} registered successfully, please check your mail to activate your account.'.format(
            user['username']), "Token": token}
        serializer.save()
        return Response(message, status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    """Allow a registered user to activate their account"""
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        """
        This method defines the get request once a user clicks on the
        activation link
        """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(username=uid)
            print(user.email)
            if user.is_active is True:
                return Response({'message': 'Activation link has expired'})
            else:
                if user is not None and jwt.decode(token,
                                                   settings.SECRET_KEY, algorithms='HS256')\
                                                   ['email']\
                                                   == user.email:
                    user.is_active = True
                    user.save()
                    # return redirect('home')
                    return Response("Thank you for your email confirmation.\
                    Now you can log into your account.")
                else:
                    return Response('Activation link is invalid!')
        except(TypeError, ValueError, OverflowError):
            user = None
            return Response("There is no such user."+str(user))


class LoginAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({"message": "login success, welcome "+user["email"]},
                            status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class SocialAuthAPIView(APIView):
    """Allow user to login via Google, Twitter and Facebook"""
    pass


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
