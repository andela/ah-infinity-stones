from rest_framework.test import APIClient
from django.test import TestCase


class BaseSetUp(TestCase):
    """Base class for all the test classes"""

    def __init__(self):
        """Initialize test data"""
        self.client = APIClient()
        self.reg_data = {'user': {
            'username': 'remmy',
            'email': 'remmy@test.com',
            'password': '@Password123'
        }}
        # register a user
        self.client.post(
            'api/users',
            self.reg_data,
            format="json")
