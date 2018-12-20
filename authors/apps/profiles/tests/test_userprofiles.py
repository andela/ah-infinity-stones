from rest_framework import status
from .base_test import BaseTestCase


class TestProfile(BaseTestCase):
    """Test the User profile GET responses"""

    all_profiles_url = 'http://127.0.0.1:8000/api/profiles/'
    my_profile_url = 'http://127.0.0.1:8000/api/profiles/jane'

    def test_get_all_profiles_without_account_activation(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.all_profiles_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Your account is disabled', str(response.data))

    def test_get_all_profiles_without_login2(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_my_profiles_without_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(self.my_profile_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_my_profiles_without_login2(self):
        response = self.client.put(self.my_profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

