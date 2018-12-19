"""This module runs tests for user login process via
Facebook, Twitter or Google
"""
import os
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class UserTestCase(TestCase):
    """This class contains tests for the user login process through
    Twiiter, Facebook or Google
    """

    def setUp(self):
        """This function defines variables to be used throughout the class"""
        self.client = APIClient()
        self.social_oauth_url = reverse('authentication:social_auth')
        self.oauth2_access_token = "ya29.Glt0BpfMY3SDBrh4WZ5sL-N8kOhnNfTN8Av1E6dm9l4ZH9dB_7ba-wOZ7ACl84qo-kXIgivPK_WiBUh1CL8DddlMaIJPzQ0Nyx4_dtMF_1TywpmZEyLXuVIJQh8E"
        self.oauth1_access_token = "1076314754-Q285n4m9KVoZPBs4PNCUIH8I49ZlHRAnoxEYT95 "
        self.oauth1_access_token_secret = "UX6IHUVOEvmgP1NpxjmzProrthOuUjy3qMwVWYfkCIF0o"

    def test_social_login_with_no_access_token(self):
        """This method test that a user cannot login via Google
        if there's no access_key
        """
        data = {"provider": "facebook"}
        response = self.client.post(
            self.social_oauth_url, data=data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("This field is required.",
                      response.data["errors"]["access_token"])

    def test_social_login_with_valid_access_token(self):
        """This method test that a user can login through social sites using oauth2"""
        data = {
            "provider": "google-oauth2",
            "access_token": self.oauth2_access_token
        }
        response = self.client.post(
            self.social_oauth_url, data=data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_social_login_with_invalid_provider(self):
        """ Test for invalid provider provider """
        data = {"provider": "000promaster",
                "access_token": self.oauth2_access_token}
        response = self.client.post(self.social_oauth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_social_login_for_oauth1_with_no_access_token_secret(self):
        """This method test that a user cannot login via Twitter
        if there's no access token secret
        """

        data = {"provider": "twitter",
                "access_token": self.oauth1_access_token}
        response = self.client.post(self.social_oauth_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"Please provide your secret access token",
                      response.content)

    def test_social_login_for_oauth2_with_valid_credentials(self):
        """This method test that a user can login through social sites using oauth2"""
        data = {"provider": "twitter",
                "access_token": self.oauth1_access_token,
                "access_token_secret": self.oauth1_access_token_secret}
        response = self.client.post(self.social_oauth_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
