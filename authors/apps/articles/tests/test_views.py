import jwt

from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from ..models import User
from authors.apps.authentication.tests.test_setup import BaseSetUp
from authors.apps.articles.models import (Article)
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework.test import APIClient


class CreateArticleTestCase(TestCase):
    def setUp(self):
        """Test method that runs before very test"""
        self.base = BaseSetUp()
        self.client = self.base.client
        self.user = {
            'user': {
                'username': 'remmy',
                'email': 'remmy@test.com',
                'password': '@Password123'
            }
        }
        self.article_data = {
            'art_slug': 'The-war-storry',
            'title': 'The war storry',
            'author': 1,
            'tag': ['js'],
            'description': 'Love is blind',
            'body': 'I really loved war until...',
        }

        response = self.client.post(
            reverse('authentication:register'), self.user, format="json")
        decoded = jwt.decode(
            response.data['Token'], settings.SECRET_KEY, algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        user.is_active = True
        self.token = response.data['Token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        user.save()
        self.article_url = reverse('articles:articles')
        self.filter_url =reverse('articles:search')

    def test_post_article(self):
        """Test that a logged in user can post an article"""

        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_all_articles(self):
        """Test that a user can get all articles"""
        response = self.client.get(self.article_url,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_one_article(self):
        """Test that a user can get a single articles"""
        self.client.post(self.article_url, self.article_data, format="json")
        article = Article.objects.get()
        response = self.client.get(self.article_url,
                                   kwargs={'art_slug': article.art_slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty_title(self):
        """Test that a validates that the title is not empty"""
        self.empty_title = {
            'title': '',
            'tag': ['js'],
            'description': 'Love is blind',
            'body': 'I really loved war until...',
        }
        response = self.client.post(self.article_url, self.empty_title,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field may not be blank',
                      response.content)

    def test_empty_description(self):
        """Test that a validates that the description is not empty"""

        self.empty_description = {
            'title': 'remmy',
            'tag': ['js'],
            'description': '',
            'body': 'I really loved war until...',
        }
        response = self.client.post(self.article_url, self.empty_description,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field may not be blank',
                      response.content)

    def test_empty_body(self):
        """Test that a validates that the body is not empty"""

        self.empty_body = {
            'title': 'remmy',
            'tag': ['js'],
            'description': 'yes please',
            'body': '',
        }
        response = self.client.post(self.article_url, self.empty_body,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field may not be blank',
                      response.content)

    def test_missing_title(self):
        """Test that a validates that the title field is not missing"""
        self.missing_title = {
            'tag': ['js'],
            'description': 'yes please',
            'body': '',
        }
        response = self.client.post(self.article_url, self.missing_title,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field is required',
                      response.content)

    def test_missing_tag(self):
        """Test that a validates that the tag field is not missing"""
        self.missing_tag = {
            'title': 'remmy',
            'description': 'yes please',
            'body': ''
        }
        response = self.client.post(self.article_url, self.missing_tag,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field is required',
                      response.content)

    def test_missing_body(self):
        """Test that a validates that the body field is not missing"""
        self.missing_body = {
            'title': 'remmy',
            'description': 'yes please',
            'tags': []
        }
        response = self.client.post(self.article_url, self.missing_body,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field is required',
                      response.content)

    def test_all_missing_data(self):
        """Test that a validates that all fields are not missing"""
        self.missing_fields = {
        }
        response = self.client.post(self.article_url, self.missing_fields,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field is required',
                      response.content)

    def test_user_can_update_article(self):
        """ Test that a logged in user can update an article"""
        slug = self.client.post(
            self.article_url, self.article_data, format="json").data["art_slug"]
        self.change_article = {
            'title': 'The love storry'
        }
        response = self.client.put(
            self.article_url + "/{}".format(slug), self.change_article, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'article updated successfully',
                      response.content)

    def test_user_can_delete_article(self):
        """Test that a logged in user can delete an article"""
        self.client.post(self.article_url, self.article_data, format="json")
        article = Article.objects.get()
        response = self.client.delete(
            reverse('articles:update', kwargs={'art_slug': article.art_slug}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('article deleted successfully',
                      response.data['message'])

    def test_user_can_tag_an_article(self):
        """Test user can register new tags"""
        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tag'], self.article_data.get("tag"))

    def test_view_article_tags(self):
        """Test user can be able to view tags on a given article"""
        slug = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        ).data["art_slug"]
        response = self.client.get(
            self.article_url+"/{}".format(slug),
            format="json"
        )
        self.assertEqual(response.data['tag'], self.article_data['tag'])

    def test_user_can_view_read_time(self):
        """Test that user can view time it takes to read the article"""
        self.client.post(self.article_url, self.article_data, format="json")
        article = Article.objects.get(title=self.article_data['title'])
        response = self.client.get(
            self.article_url + "/{}".format(article.art_slug), format="json")

        self.assertEqual(response.data['read_time'], 1)


class CreateCommentTestCase(TestCase):
    def setUp(self):
        self.comment_data = {'article': 1, 'user': 1, 'comment': 'Nice story '}

    def test_user_can_post_a_comment(self):
        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleShareTestCase(TestCase):
    """This class defines the api test suite for sharing articles"""

    def setUp(self):
        """Define test data and test client"""
        self.user = {
            "user": {
                "username": "paul",
                "email": "paul@test.com",
                "password": "@Password123"
            }
        }
        self.article_data = {
            "art_slug": "My-wife-my-life",
            "title": "Family Life",
            "author": 1,
            "tag": ["Marriage", "Love", "Wife", "Relationship"],
            "description": "Marriage is sweet",
            "body": "Marriage is a lifetime decision where you decide to love...",
            "read_time": 8
        }
        self.client = APIClient()
        self.jwt_auth = JWTAuthentication()
        self.reg_response = self.client.post(
            reverse("authentication:register"),
            self.user,
            format="json"
        )
        self.article_url = reverse("articles:articles")
        self.token = self.reg_response.data.get("Token")
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        user = User.objects.get(email="paul@test.com")
        user.is_active = True
        user.save()
        self.response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )

    def test_article_has_share_link_for_twitter(self):
        """User can share article on twitter"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.response.data.get("share_urls")["twitter"])
        self.assertIn("twitter", self.response.data.get(
            "share_urls")["twitter"])

    def test_article_has_share_link_for_facebook(self):
        """User can share article on facebook"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.response.data.get("share_urls")["facebook"])
        self.assertIn("facebook", self.response.data.get(
            "share_urls")["facebook"]
        )

    def test_article_has_share_link_for_email(self):
        """User can share article via email"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.response.data.get("share_urls")["email"])
        self.assertIn("mailto", self.response.data.get(
            "share_urls")["email"]
        )


class ArticleRatingTestCase(TestCase):
    """This class defines the api to article rating test case"""

    def setUp(self):
        """Set or initialize the test data"""
        self.rating = {"article": 1, "author": 1, "rating": 5}

    def test_user_can_rate_an_article(self):
        """Test user can rate articles"""
        # add article
        self.article = {
            "title": "The mighty king",
            "author": 1,
            "tag": [1],
            "description": "Killed a lion with a sword",
            "body": "The JUJU king has done it again...",
            "read_time": 4
        }
        self.client.post("api/articles/", self.article, format="json")
        # Rate article
        response = self.client.post(
            "api/articles/ratings", self.rating, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get average ratings average rating for their articles
        response = self.client.post(
            "api/articles/user_ratings/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ Add the following code when ratings feature is implemented
            self.assertEqual(response.data['ratings'], 5)
        """


class ArticleLikeDisklikeTestCase(TestCase):
    """This class defines the api test case to like or dislike articles"""

    def setUp(self):
        """Set or initialize the test data"""
        # add article
        self.article = {
            "title": "The killer disease",
            "author": 1,
            "tag": [1],
            "description": "HIV revisited",
            "body": "Handily did they love him until he was no more...",
            "read_time": 2
        }
        self.like = {"article": 1, "user": 1, "like": True}
        self.client.post("api/articles", self.article, format="json")
        response = self.client.post(
            "api/articles/likes", self.like, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleFavoriteTestCase(TestCase):
    """This class defines the api test case to favorite articles"""

    def setUp(self):
        """Set or initialize the test data"""
        # add article
        self.article = {
            "title": "Life Hack Guide",
            "author": 1,
            "tag": [1],
            "description": "Discorer you life in 3 minutes.",
            "body": "Many people still do not to know what they value in life",
            "read_time": 3
        }
        self.favorite = {"article": 1, "user": 1, "favorite": True}
        self.client.post("api/articles", self.article, format="json")
        response = self.client.post(
            "api/articles/favorites", self.favorite, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleSearchTest(CreateArticleTestCase):
    def test_user_can_filter_article_by_author(self):
        """ Test user is able to filter articles by author name"""
        # post one article
        self.client.post(self.article_url, self.article_data, format="json")
        self.article_data_2 = {
            'title': 'How to train your mind',
            'author': 1,
            'tag': ['philosophy'],
            'description': 'How can your mind train itself?',
            'body': 'Its actually possible, your mind is not you'
                    'so basically its you training the mind...',
            'read_time': 3
        }
        author = self.user['user']['username']
        # post a second article
        self.client.post(self.article_url, self.article_data, format="json")
        response = self.client.get(
            self.filter_url + '?author={}'.format(author), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_search_article(self):
        """ Test user can search articles by keywords"""
        self.client.post(self.article_url, self.article_data, format="json")
        self.article_data_2 = {
            'title': 'How to train your mind',
            'author': 1,
            'tag': ['philosophy'],
            'description': 'How can your mind train itself?',
            'body': 'Its actually possible, your mind is not you'
                    'so basically its you training the mind...',
            'read_time': 3
        }
        # post a second article
        self.client.post(self.article_url, self.article_data, format="json")
        response = self.client.get(self.filter_url+ '?q=mind', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
