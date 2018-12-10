import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .test_setup import BaseSetUp


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base = BaseSetUp()

        self.login_data = {
            "username": "remmy",
            "password": "hgfhdbfsjhb"
        }
        self.reg_url = reverse('authentication:register')

    def test_register_user_successfully(self):
        """Test that checks if a user instance is created."""

        response = self.client.post(
            self.reg_url,
            self.base.reg_data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b"successfully", response.content)

    def test_empty_username_field(self):
        """Test that checks if the username input is empty."""
        self.empty_username = {'user': {
            "username": "",
            "email": "remmy@test.com",
            "password": "Password123"
        }}

        response = self.client.post(
            self.reg_url,
            self.empty_username,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"may not be blank", response.content)

    def test_empty_email_field(self):
        """Test that checks if the email input is empty."""
        self.empty_email = {'user': {
            "username": "remmy",
            "email": "",
            "password": "Password123"
        }}

        response = self.client.post(
            self.reg_url,
            self.empty_email,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"may not be blank", response.content)

    def test_empty_password_field(self):
        """Test that checks if the password input is empty."""
        self.empty_password = {'user': {
            "username": "remmy",
            "email": "remmy@test.com",
            "password": ""
        }
        }

        response = self.client.post(
            self.reg_url,
            self.empty_password,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"may not be blank", response.content)

    def test_valid_username(self):
        """Test that checks if the username has valid input."""
        self.valid_username = {'user': {
            "username": "1@1#%^()+",
            "email": "remmytest.com",
            "password": "Password123"
        }}

        response = self.client.post(
            self.reg_url,
            self.valid_username,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"can only contain letters, numbers, -, _",
                      response.content)

    def test_valid_email(self):
        """Test that checks if the email has valid input."""
        self.valid_email = {'user': {
            "username": "remmy",
            "email": "remmytest.com",
            "password": "Password123"
        }
        }
        response = self.client.post(
            self.reg_url,
            self.valid_email,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"must be in the format xxxx@xxxx.xx", response.content)

    def test_invalid_password(self):
        """Test that checks if the password has valid input."""
        self.valid_password = {'user': {
            "username": "remmyk",
            "email": "remmyk@test.com",
            "password": "1234567890"
        }
        }
        response = self.client.post(
            self.reg_url,
            self.valid_password,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"between 8-128 chars long and must", response.content)

    def test_duplicate_username(self):
        """Test that checks if the username already exists."""
        self.duplicate_username = {'user': {
            "username": "remmy",
            "email": "remmy@test.com",
            "password": "@Password123"
        }}

        self.duplicate_username2 = {'user': {
            "username": "remmy",
            "email": "remmyk@test.com",
            "password": "@Password123"
        }}

        self.client.post(
            self.reg_url,
            self.duplicate_username,
            format="json")

        response = self.client.post(
            self.reg_url,
            self.duplicate_username2,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"Username provided already in use", response.content)

    def test_duplicate_email(self):
        """Test that checks if the email already exists."""
        self.duplicate_email = {'user': {
            "username": "remmy",
            "email": "remmyk@test.com",
            "password": "@Password123"
        }}

        self.duplicate_email2 = {'user': {
            "username": "remmyk",
            "email": "remmyk@test.com",
            "password": "@Password123"
        }
        }
        self.client.post(
            self.reg_url,
            self.duplicate_email,
            format="json")
        response = self.client.post(
            self.reg_url,
            self.duplicate_email2,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"email provided is already in use", response.content)

    def test_missing_data(self):
        """Test that checks if the required fields exists."""

        response = self.client.post(
            self.reg_url,
            {},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"required", response.content)

    def test_missing_username(self):
        """Test that checks if the required username field exists."""
        self.missing_username = {
            "email": "remmyk@testcom",
            "password": "@Password123"
        }

        response = self.client.post(
            self.reg_url,
            self.missing_username,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"required", response.content)

    def test_missing_email(self):
        """Test that checks if the required email field exists."""
        self.missing_email = {
            "username": "remmy",
            "password": "@Password123"
        }

        response = self.client.post(
            self.reg_url,
            self.missing_email,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"required", response.content)

    def test_missing_password(self):
        """ Test that checks if the required password field exists."""
        self.missing_password = {
            "username": "remmyk",
            "email": "remmyk@testcom",
        }

        response = self.client.post(
            self.reg_url,
            self.missing_password,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"required", response.content)
