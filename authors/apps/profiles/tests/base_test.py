from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
import json


class BaseTestCase(TestCase):
    """
    The base test case that all the test classes will use throughout
    the app
    """
    register_url = 'http://127.0.0.1:8000/api/users/'
    login_url = 'http://127.0.0.1:8000/api/users/login/'

    def setUp(self):
        self.client = APIClient()

        self.reg_url = reverse('authentication:register')
        self.profile_url = reverse('profiles:profile')

        self.one_user = {
            "user": {
                'email': 'leo@example.com',
                'username': 'leon',
                'password': 'leoN_$2300'
            }
        }

        self.two_user = {
            "user": {
                'email': 'eliza@example.com',
                'username': 'eliza',
                'password': 'elizA_$1400'
            }
        }

        self.tri_user = {
            "user": {
                'email': 'johnny@example.com',
                'username': 'johnny',
                'password': 'johnnY_$1000'
            }
        }

        self.foo_user = {
            "user": {
                'email': 'obama@example.com',
                'username': 'obama',
                'password': 'obamA_$4300'
            }
        }
        response = self.client.post(self.reg_url, self.tri_user, format="json")
        result = response.content
        result = json.loads(result.decode('utf-8'))
        self.token = result["user"]["Token"]
        self.msg = result["user"]["Message"]

    def test_registration(self):
        self.assertIn('johnny registered successfully', self.msg)
