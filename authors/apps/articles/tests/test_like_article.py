import jwt
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from ..models import User


class LikeDislike(TestCase):
    """ Test LikeDislike class"""

    def setUp(self):
        self.client = APIClient()
        self.user = {"user": {
            "username": "justo",
            "email": "justinjustin@yahoo.co.ke",
            "password": "@Password1"

        }
        }
        res = self.client.post(
            reverse('authentication:register'), self.user, format="json")
        decoded = jwt.decode(
            res.data['Token'], settings.SECRET_KEY, algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        user.is_active = True
        user.save()

        self.token = res.data['Token']
        self.client.credentials(HTTP_AUTHORIZATION=res.data['Token'])
        self.article_url = reverse('articles:articles')
        self.article_data = {
            "title": "doing it",
            "tag": ["doing"],
            "description": "doing it",
            "body": "This is how we do it",
            "read_time": 3
        }
        self.client.post(self.article_url, self.article_data, format="json")
        self.slug = 'doing-it'
        self.like_url = reverse(
            'articles:like_article', kwargs={'art_slug': self.slug})
        self.like = {'like': 'True'}
        self.dislike = {'like': 'False'}
        self.slug_404 = '404'
        self.like_404_url = reverse(
            'articles:like_article', kwargs={'art_slug': self.slug_404})

    def test_can_like_an_article(self):
        """ Test user can like an article"""
        response = self.client.post(self.like_url,
                                    data=self.like,
                                    format="json",
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_like_404_article(self):
        """ Test cannot like non existing article"""
        response = self.client.post(self.like_404_url,
                                    data=self.like,
                                    format="json",
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_dislike_an_article(self):
        """ Test user can dislike an article"""
        response = self.client.post(self.like_url,
                                    data=self.dislike,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_like_article_unauthorized(self):
        """ Test user needs to login to like"""
        self.client.credentials()
        response = self.client.post(self.like_url,
                                    data=self.like,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
