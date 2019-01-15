"""This module runs tests for user login process"""
from django.conf import settings
import json
import jwt
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .test_setup import BaseSetUp
from authors.apps.authentication.backends import JWTAuthentication
from ..models import User


class UserTestCase(TestCase):
    """This class contains tests for the user login process wihtout
    social authentication
    """

    def setUp(self):
        """This function defines variables tobe used within the class"""
        self.base = BaseSetUp()
        self.client = self.base.client
        self.user = {"user": {
            "email": "remmy@test.com",
            "username": "remmy",
            "password": "@Password123"
        }}

        self.test_password = {"user": {
            "email": "remmy@test.com",
            "password": "passssssss"
        }}
        res = self.client.post(
            reverse('authentication:register'), self.user, format="json")
        decoded = jwt.decode(
            res.data['Token'], settings.SECRET_KEY, algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        user.is_active = True
        user.save()

    def test_login_user(self):
        """This function tests whether a registered user can login"""
        self.login_details = {
            "user":{
                "email": self.user['user']['email'],
                "password": self.user['user']['password']
            }
        }
        # Login response
        self.response = self.client.post(
            reverse("authentication:login"),
            self.login_details,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertIn("Login successful", self.response.data['Message'])

    def test_cannot_login_unregistered_user(self):
        """This function tests whether an unregistered user can login"""
        self.user = {"user": {
            "email": "xxxxhn@doe.com",
            "password": "Passwo8urd@123"
        }}
        response = self.client.post(
            reverse("authentication:login"),
            self.user,
            format="json"
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with this email and password was not found.", response.data['errors']['error'])

    def test_cannot_login_user_with_wrong_password(self):
        """This function tests whether a registered user can login with
        wrong password
        """
        user = User.objects.get(email="remmy@test.com")
        user.is_active = True
        user.save()
        response = self.client.post(
            reverse("authentication:login"),
            self.test_password,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b"A user with this email and password was not found.", response.content)
