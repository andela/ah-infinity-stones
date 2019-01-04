from rest_framework import status
from .base_test import BaseTestCase


class TestProfile(BaseTestCase):
    """Test the Article Comments responses"""

    all_comments_url = '/api/comments/'
    one_comment_url = '/api/comments/1/'

    def test_get_all_comments_without_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.all_comments_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_all_comments_without_login2(self):
        response = self.client.get(self.all_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_my_comment_without_login(self):
        response = self.client.put(self.one_comment_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_comment_without_login2(self):
        response = self.client.put(self.one_comment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_my_comment_with_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(self.one_comment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_my_comment_without_login(self):
        response = self.client.delete(self.one_comment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

