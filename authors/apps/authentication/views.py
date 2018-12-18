from __future__ import unicode_literals
import jwt
from rest_framework import status
from rest_framework.generics import (CreateAPIView)
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils.encoding import force_text
from rest_framework import authentication
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from datetime import datetime, timedelta
from authors.apps.authentication.backends import JWTAuthentication
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.views.generic import TemplateView
from django.contrib.auth import user_logged_in
from requests.exceptions import HTTPError
from django.core.mail import send_mail
from rest_framework.generics import RetrieveUpdateAPIView
from django.template.loader import render_to_string
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import AuthAlreadyAssociated
from .models import User
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UserSerializer, SocialAuthSerializer,
                          ResetQuestSerializer)
from ...settings import EMAIL_HOST_USER


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        """
        Generate and return a decoded token.
        """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        date_time = datetime.now() + timedelta(days=2)
        payload = {
            'email': user['email'],
            'exp': int(date_time.strftime('%s'))
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        token = token.decode('utf-8')
        domain = '127.0.0.1:8000'
        self.uid = urlsafe_base64_encode(force_bytes(
            user['username'])).decode("utf-8")
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        domain = '127.0.0.1:8000'
        self.uid = urlsafe_base64_encode(force_bytes(
            user['username'])).decode("utf-8")
        time = datetime.now()
        time = datetime.strftime(time, '%d-%B-%Y %H:%M')
        message = render_to_string(
            'email_confirm.html', {
                'user':
                user,
                'domain':
                domain,
                'uid':
                self.uid,
                'token':
                token,
                'username':
                user['username'],
                'time':
                time,
                'link':
                'http://' + domain + '/api/user/activate/' + self.uid + '/' +
                token + '/'
            })
        mail_subject = 'Activate your account.'
        to_email = user['email']
        from_email = 'infinitystones.team@gmail.com'
        send_mail(
            mail_subject,
            'Verify your Account',
            from_email, [
                to_email,
            ],
            html_message=message,
            fail_silently=False)

        message = {
            'Message':
            '{} registered successfully, please check your mail to activate your account.'
            .format(user['username']),
            "Token":
            token
        }
        serializer.save()
        return Response(message, status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    """Allow a registered user to activate their account"""
    permission_classes = (AllowAny, )

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
                                                   settings.SECRET_KEY, algorithms='HS256')['email']\
                        == user.email:
                    user.is_active = True
                    user.save()
                    # return redirect('home')
                    return Response("Thank you for your email confirmation.\
                    Now you can log into your account.")
                else:
                    return Response('Activation link is invalid!')
        except (TypeError, ValueError, OverflowError):
            user = None
            return Response("There is no such user." + str(user))


class LoginAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_class = (JWTAuthentication, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        email = user['email']
        return Response(
            {
                "Message": "Login successful, welcome {} ".format(email)
            },
            status=status.HTTP_200_OK)
        return JsonResponse(
            {
                "message": "login success, welcome " + user["email"]
            },
            status=status.HTTP_200_OK)


class SocialAuthAPIView(APIView):
    """Allow user to login via Google, Twitter and Facebook"""
    pass


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)


class SocialAuthAPIView(CreateAPIView):
    """This class allows users to login through Social sites such as
     Google, Twitter, and Facebook"""
    permission_classes = (AllowAny, )
    serializer_class = SocialAuthSerializer
    renderer_classes = (UserJSONRenderer, )

    def create(self, request, *args, **kwargs):
        """Get social auth provider and token and generates the user token based on the user
         email"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt_auth = JWTAuthentication()
        # If login request is made by an already existing user, associate the request with their account.
        authenticated_user = request.user if not request.user.is_anonymous else None
        try:
            # Validate provider in the backend.
            backend = load_backend(
                strategy=load_strategy(request),
                name=serializer.data.get("provider"),
                redirect_uri=None)
            if isinstance(backend, BaseOAuth1):
                # Get access_token and secret access token for providers using BaseOAuth1
                if "access_token_secret" in request.data:
                    token = {
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret':
                        request.data['access_token_secret']
                    }
                else:
                    return Response(
                        {
                            "error": "Please provide your secret access token"
                        },
                        status=status.HTTP_400_BAD_REQUEST)
            elif isinstance(backend, BaseOAuth2):
                # Get access_token for providers using BaseOAuth2
                token = serializer.data.get("access_token")
        except MissingBackend:
            return Response({
                "error": "Please enter a valid provider"
            },
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = backend.do_auth(token, user=authenticated_user)

        except BaseException as error:
            return Response({"error": str(error)})
        if user and user.is_active:
            user.is_active = True
            # Serialize the user and get the user details.
            user.save()
        serializer = UserSerializer(user)
        serialized_data = serializer.data
        serialized_data["token"] = jwt_auth.generate_token(
            serialized_data["email"], serialized_data["username"])
        return Response(serialized_data, status=status.HTTP_200_OK)
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetBymailAPIView(CreateAPIView):
    # Allow user to reset password via mail
    serializer_class = ResetQuestSerializer

    def post(self, request):
        user_name = request.data['user']
        serializer = self.serializer_class.validate_email_data(data=user_name)

        # format the email
        hosting = request.get_host()
        if request.is_secure():
            response = "https://"
        else:
            response = "http://"
        resetpage = response + hosting + 'api/reset_password/'
        subject = "You requested password reset"
        message = "Hello {user_name} you requested for a change in your \n"
        "password.Please click on the link bellow to continue \n\n{link}\n\n."
        "If this was not \n"
        "you Please ignore the message. ".format(user_data=user_name['email'])
        "you Please ignore the message. ".format(user_data=user_name['email'])
        from_email = EMAIL_HOST_USER
        to_list = [user_name['email']]

        # send the email to user

        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Response to the user
        return Response(
            {
                "message": "Please check your email for password reset link"
            },
            status=status.HTTP_200_OK)
