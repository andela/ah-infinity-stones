"""This module runs tests for user login process via
Facebook, Twitter or Google
"""
import os
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class UserTestCase(TestCase):
    """This class contains tests for the user login process through
    Twiiter, Facebook or Google
    """

    def setUp(self):
        """This function defines variables to be used throughout the class"""
        self.client = APIClient()
        self.google_key = os.getenv('GOOGLE_KEY')
        self.google_secret = os.getenv('GOOGLE_SECRET')
        self.facebook_key = os.getenv('FACEBOOK_KEY')
        self.facebook_secret = os.getenv('FACEBOOK_SECRET')
        self.twitter_key = os.getenv('TWITTER_KEY')
        self.twitter_secret = os.getenv('TWITTER_SECRET')

    def test_google_login_no_access_key(self):
        """This method test that a user cannot login via Google
        if there's no access_key
        """

        data = {"provider": "google",
                "access_key_secret": self.google_secret}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Google access_key is missing")
        self.assertEqual(json.loads(response.data)["token"], None)

    def test_google_login_no_access_key_secret(self):
        """This method test that a user cannot login via Google
        if there's no access_key_secret
        """
        data = {"provider": "google",
                "access_key": self.google_key}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Google access_key_secret is missing")
        self.assertEqual(json.loads(response.data)["token"], None)

    def test_google_login(self):
        """This method test that a user can login through google"""
        data = {"provider": "google",
                "access_key": self.google_key,
                "access_key_secret": self.google_secret}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data)["message"],
                         "User logged in successfully.")
        self.assertNotEqual(json.loads(response.data)["token"], None)

    def test_twitter_login_no_access_key(self):
        """This method test that a user cannot login via Twitter
        if there's no access_key
        """

        data = {"provider": "twitter",
                "access_key_secret": self.twitter_secret}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Twitter access_key is missing")
        self.assertEqual(json.loads(response.data)["token"], None)

    def test_twitter_login_no_access_key_secret(self):
        """This method test that a user cannot login via Twitter
        if there's no access_key_secret
        """

        data = {"provider": "twitter",
                "access_key": self.twitter_key}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Twitter access_key_secret is missing")
        self.assertEqual(json.loads(response.data)["token"], None)

    def test_twitter_login(self):
        """This method test that a user can login through twitter"""
        data = {"provider": "twitter",
                "access_key": self.twitter_key,
                "access_key_secret": self.twitter_secret}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data)["message"],
                         "User logged in successfully.")
        self.assertNotEqual(json.loads(response.data)["token"], None)

    def test_facebook_login_no_access_key(self):
        """This method test that a user cannot login via Facebook
        if there's no access_key
        """
        data = {"provider": "facebook",
                "access_key_secret": self.facebook_secret}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Facebook access_key is missing")
        self.assertEqual(json.loads(response.data)["token"], None)

    def test_facebook_login_no_access_key_secret(self):
        """This method test that a user cannot login via Facebook
        if there's no access_key_secret
        """
        data = {"provider": "facebook",
                "access_key": self.facebook_key}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Facebook access_key_secret is missing")
        self.assertEqual(json.loads(response.data)["token"], None)

    def test_facebook_login(self):
        """This method test that a user can login through Facebook"""
        data = {"provider": "facebook",
                "access_key": self.facebook_key,
                "access_key_secret": self.facebook_secret}
        response = self.client.post('api/socialAuth', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data)["message"],
                         "User logged in successfully.")
        self.assertNotEqual(json.loads(response.data)["token"], None)
