"""Module houses tests for notifications"""
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Notification
from ...authentication.tests.test_setup import BaseSetUp
from django.test import TestCase


class SetUp(TestCase):
    """Base setup class to be shared by other test classess"""

    def setUp(self):
        """Initialize test data"""
        self.base = BaseSetUp()
        self.login_data = {
            'username': self.base.reg_data['username'],
            'password': self.base.reg_data['password']
        }
        # login a test user and generate token
        self.login_res = self.base.client.post(
            'api/users/login',
            self.login_data,
            format="json")
        self.token = self.login_res.data['Token']
        # pass token to test client to authorize api access
        self.base.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.update_data = {"read": True}


class TestNotificationModel(SetUp):
    """Tests for the Notification Model"""

    def test_object_creation(self):
        """Test api can create a notification object"""
        self.notify_title = "Article published"
        self.notifications = Notification(title=self.notify_title)
        initial_count = Notification.objects.count()
        self.notifications.save()
        final_count = Notification.objects.count()
        self.assertEqual(final_count - initial_count, 1)
        self.assertEqual(Notification.objects.get().title, 'Article published')


class TestNotificationView(SetUp):
    """Tests for the Notification views"""

    def test_fetch_notifications(self):
        """Test user can get all notifications"""
        response = self.base.client.get(
            "/api/notifications/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_one_notification(self):
        """Test user can get single notification"""
        response = self.base.client.get(
            "/api/notifications/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_unauthorized_notification(self):
        """Test only authorized users can get notifications"""
        # clear the client authorization inherited from SetUp first
        self.base.client.credentials()
        response = self.base.client.get(
            "/api/notifications/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_article_notifications(self):
        """Test user can get all article notifications"""
        response = self.base.client.get(
            "/api/notifications/articles", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_comment_notifications(self):
        """Test user can get all comment notifications"""
        response = self.base.client.get(
            "/api/notifications/comments", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_profile_notifications(self):
        """Test user can get all profile notifications"""
        response = self.base.client.get(
            "/api/notifications/profile", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_nonexist_notification(self):
        """Test only existing notification can be viewed"""
        response = self.base.client.get(
            "/api/notifications/100001", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_subscribe(self):
        """Tests user can subscribe to all notifications"""
        response = self.base.client.get(
            "/api/notifications/subscribe", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "Successfully subscribed to notifications", response.message)

    def test_user_can_subscribe_email(self):
        """Tests user can subscribe to email notifications"""
        response = self.base.client.get(
            "/api/notifications/subscribe/email", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("subscribed to email", response.message)

    def test_user_can_subscribe_in_app(self):
        """Tests user can subscribe to in-app notifications"""
        response = self.base.client.get(
            "/api/notifications/subscribe/in-app", format="json")
        self.assertIn("subscribed to in-app", response.message)

    def test_user_can_unsubscribe(self):
        """Tests user can unsubscribe from notifications"""
        response = self.base.client.get(
            "/api/notifications/unsubscribe", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "Successfully unsubscribed to notifications", response.message)

    def test_user_can_unsubscribe_email(self):
        """Tests user can unsubscribe from email notifications"""
        response = self.base.client.get(
            "/api/notifications/unsubscribe/email", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("unsubscribed from email", response.message)

    def test_user_can_unsubscribe_in_app(self):
        """Tests user can unsubscribe from in-app notifications"""
        response = self.base.client.get(
            "/api/notifications/unsubscribe/in-app", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("unsubscribed from in-app", response.message)


class NotificationTestCaseDeleteUpdate(SetUp):
    """Tests class for the delete and update"""

    def test_can_update_one_notification(self):
        """
        Test can update a notifications
        """
        response = self.base.client.put(
            "/api/notifications/1", self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_unexisting_notification(self):
        """
        Test cannot update a notifications
        """
        response = self.base.client.put(
            "/api/notifications/100000001", self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete_one_notification(self):
        """
        Test can delete a notification
        """
        response = self.base.client.delete(
            "/api/notifications/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_unexisting_notification(self):
        """
        Test cannot delete a notification
        """
        response = self.base.client.delete(
            "/api/notifications/100000001", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
