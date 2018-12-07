"""Module tests creation and fecthing of notifications"""
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Notification
from ...authentication.tests.test_setup import BaseSetUp


class TestNotificationModel(BaseSetUp):
    """Tests for the Notification Model"""

    def test_object_creation(self):
        """Test api can create a notification object"""
        self.notify_title = "Article published"
        self.notifications = Notification(title=self.notify_title)
        initial_count = Notification.objects.count()
        self.notifications.save()
        final_count = Notification.objects.count()
        self.assertEqual(final_count - initial_count, 1)


class TestNotificationView(BaseSetUp):
    """Tests for the Notification views"""

    def test_fetch_notifications(self):
        """Test user can get all notifications"""
        # ensure user is logged in first
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(
            "/api/notifications/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_one_notification(self):
        """Test user can get single notification"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(
            "/api/notifications/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_unauthorized_notification(self):
        """Test user cannot get notification unauthorized"""
        response = self.client.get(
            "/api/notifications/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_article_notifications(self):
        """Test user can get all article notifications"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(
            "/api/notifications/articles", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_comment_notifications(self):
        """Test user can get all comment notifications"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(
            "/api/notifications/comments", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_profile_notifications(self):
        """Test user can get all profile notifications"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(
            "/api/notifications/profile", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_nonexist_notification(self):
        """Test user cannnot get nonexisting notification"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(
            "/api/notifications/100001", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NotificationTestCaseDeleteUpdate(BaseSetUp):
    """Tests class for the delete and update"""
    
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


