from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.core import mail
from django.urls import reverse
import jwt
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from ..models import User


class TestPasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = {
            'user': {
                "email": "domisemak@yahoo.co.uk",
                "username": "domisemak",
                "password": "@P3assword"
            }
        }
        self.forgot_password = {
            "email": "domisemak@yahoo.co.uk",
        }
        # register and activate user account
        res = self.client.post(
            reverse('authentication:register'), self.user, format="json")
        # import pdb
        # pdb.set_trace()
        decoded = jwt.decode(
            res.data['Token'], settings.SECRET_KEY, algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        pk = urlsafe_base64_encode(force_bytes(user.id)).decode()
        url = 'http://127.0.0.1:8000/api/user/activate/{pk}/{token}'.format(
            pk=pk, token=res.data['Token'])
        self.client.get(url)

    def test_send_forgot_password_mail(self):
        """Test that checks if a reset password mail is sent"""

        response = self.client.post(
            reverse('authentication:reset'),
            self.forgot_password,
            format="json")
        self.assertIn(b'please check your mail for password reset link',
                      response.content)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        """Test that checks if a user who forgot their password can reset it"""
        self.reset_password = {"password": "Password123"}
        response = self.client.post(
            reverse('authentication:reset'),
            self.forgot_password,
            format="json")
        response = self.client.put(
            reverse(
                'authentication:update_password',
                kwargs={'token': response.data['Token']}),
            self.reset_password,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"successfully updated", response.content)