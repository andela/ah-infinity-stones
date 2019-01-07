from rest_framework import status
from django.http import HttpResponsePermanentRedirect
from .base_test import BaseTestCase


class TestProfile(BaseTestCase):
    """Test the User profile GET responses"""

    one_bookmark_url = 'http://127.0.0.1:8000/api/articles/i-hate-homos/bookmark'
    my_bookmarks_url = 'http://127.0.0.1:8000/api/bookmarks'

    def test_add_bookmark_without_valid_account(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.one_bookmark_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_bookmarks_without_login(self):
        response = self.client.get(self.one_bookmark_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_bookmarks_without_account_activation(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.my_bookmarks_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response, HttpResponsePermanentRedirect))

    def test_cannot_delete_unexisting_bookmark(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(self.one_bookmark_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


