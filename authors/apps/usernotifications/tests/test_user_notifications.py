import json

from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from notifications.signals import notify
from rest_framework import status
from django.contrib.auth import get_user_model

# local imports
from authors.apps.authentication.models import User
from ..models import Notification
from ..models import Article


class NotificationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # data for user creation
        self.one_user_data = {
            'username': 'theo',
            'email': 'theo@localhost.com',
            'password': '$_0007'
        }
        self.two_user_data = {
            'username': 'eliza',
            'email': 'eliza@localhost.com',
            'password': '$_0014'
        }
        self.test_user_data = {
            'username': 'angela',
            'email': 'angela@localhost.com',
            'password': '$_0017'
        }

        # data for article creation
        self.one_article_data = {
            'title': 'rony buys a  yacht',
            'description': 'sea life is good',
            'body': 'rony was last seen going on a vacation with his new found love, not a woman',
            'tags': ['rony', 'yacht', 'vacation']
        }
        self.two_article_data = {
            'title': 'promaster shot in a temple',
            'description': 'shot but alive',
            'body': 'kung fu master paul cheung mathenge aka promaster insisted on martial arts before receiving 4 rounds',
            'tags': ['kungfu', 'shaolin', 'rounds']
        }

        # data for comment creation
        self.one_comment_data = {
            'body':'I loved reading your article'
        }
        self.two_comment_data = {
            'body':'Too much salt in paragraph two. Had lots of fun'
        }


        # split data for user
        self.one_username = "theo"
        self.one_email = "theo@localhost.com"
        self.one_password = "$_0007"

        self.two_username = "eliza"
        self.two_email = "eliza@localhost.com"
        self.two_password = "$_0014"
        
        self.test_username = "angela"
        self.test_email = "angela@localhost.com"
        self.test_password = "$_0017"


        # data for user login
        self.one_login_data = {
                "email": self.one_email,
                "password": self.one_password
        }
        self.two_login_data = {
                "email": self.two_email,
                "password": self.two_password
        }
        self.test_login_data = {
                "email": self.test_email,
                "password": self.test_password
        }
        # create user
        self.client.post(
        'api/users/register',
        self.one_user_data,
        format="json")

        # user login
        self.login_response = self.client.post(
            'api/users/register', self.one_user_data, format="json")
        self.user_token = self.login_response
        # create notification object
        self.notify_title = "Justo followed you"
        self.notifications = Notification(title=self.notify_title)
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
            eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.\
            SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"        

    def create_notifications(self):
        """
        create notification instances
        """
        user = get_user_model().objects.get(email=self.one_user_data["email"])
        notify.send(user, recipient=user, verb='you reached level 10')


    # actual tests
    def test_can_update_one_notification(self):
        """
        Test can update a notifications
        """
        self.data = {"read": True}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(
            "/api/notifications/1", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_unexisting_notification(self):
        """
        Test cannot update a notifications
        """
        self.data = {"read": True}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(
            "/api/notifications/100000001", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete_one_notification(self):
        """
        Test can delete a notification
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(
            "/api/notifications/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_unexisting_notification(self):
        """
        Test cannot delete a notification
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(
            "/api/notifications/100000001", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



