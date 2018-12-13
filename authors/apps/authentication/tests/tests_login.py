"""This module runs tests for user login process"""
import json
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
        self.email = "remmy@test.com"
        self.username = "remmy"
        self.token = JWTAuthentication.generate_token(
            self, email=self.email, username=self.username)
        self.user = {"user": {
            "email": "remmy@test.com",
            "password": "Password123"
        }}

        self.test_password = {"user": {
            "email": "remmy@test.com",
            "password": "passssssss"
        }}
        # Registration response
        self.resp = self.client.post(
            reverse("authentication:register"),
            self.base.reg_data,
            format="json")

    def test_login_user(self):
        """This function tests whether a registered user can login"""
        # Test user registration
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.resp.data["Message"],
                         "remmy registered successfully, please check your mail to activate your account.")

        # Login response
        self.response = self.client.post(
            reverse("authentication:login"),
            self.user,
            format="json",
            HTTP_AUTHORIZATION=self.resp.data["Token"]
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            self.response.data["detail"], "Your account is disabled, please"
            " visit your email to activate your account")

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
                         status.HTTP_403_FORBIDDEN)
        self.assertIn(response.data["detail"],
                      "Authentication credentials were not provided.")

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
            format="json",
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b"A user with this email and password was not found.", response.content)
