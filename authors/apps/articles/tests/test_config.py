from rest_framework.test import APIClient
from django.test import TestCase

from .test_data import generate_test_data


class MainTestConfig(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        generate_test_data()

        cls.client = APIClient()
