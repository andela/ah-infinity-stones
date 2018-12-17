import jwt

from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from ..models import User
from authors.apps.authentication.tests.test_setup import BaseSetUp
from authors.apps.articles.models import (Article)


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

    def test_post_article(self):
        """Test that a logged in user can post an article"""
        response = self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_can_get_an_article(self):
        self.client.post(
            self.article_url,
            self.article_data,
            format="json"
        )
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
        self.client.post(self.article_url, self.article_data, format="json")
        article = Article.objects.get()
        self.change_article = {'title': 'The love storry'}
        response = self.client.put(
            reverse('articles:update', kwargs={'art_slug': article.art_slug}),
            self.change_article,
            format='json')
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


class CreateCommentTestCase(TestCase):
    def setUp(self):
        self.comment_data = {'article': 1, 'user': 1, 'comment': 'Nice story '}

    def test_user_can_post_a_comment(self):
        response = self.client.post(
            reverse('comment'), self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_all_comments(self):
        response = self.client.get(reverse('all_comments', ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArticleTagsTestCase(TestCase):
    """This class defines the api for Tag CRUD methods"""

    def setUp(self):
        """"This method sets the test variables and test client"""
        self.base = BaseSetUp()
        self.client = self.base.client
        # Initialize login credentials
        self.login_data = {
            "username": "remmy@test.com",
            "password": "Password123"
        }
        # Declare login response
        self.login_response = self.client.post(
            "api/users/login", self.login_data, format="json")
        # Replace the dummy token with self.login_response.data["Token"]
        self.token = "eSknaojdIdlafesodoilkjdalfdJndajfdaljfeESFdafjdalfjaofje"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_user_can_create_tag(self):
        """Test user can register new tags"""
        self.tag_data = {"tag": "Python"}
        response = self.client.post(
            "api/articles/tags", self.tag_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_specific_tag(self):
        """Test api can return specific tag"""
        response = self.client.get("api/articles/tags/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_all_tag(self):
        """Test api can return all tags to enable easy filtering of articles"""
        response = self.client.get("api/articles/tags", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_specific_tag(self):
        """Test api can update a specific tag"""
        self.new_data = {"tag": "Love"}
        response = self.client.put(
            "api/articles/tags/1", self.new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_specific_tag(self):
        """Test api can delete specific tag"""
        response = self.client.get("api/articles/tags/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_tag_an_article(self):
        """Test api can add tag to an article"""
        # add a new tag
        self.new_data = {"tag": "Marriage"}
        self.client.post("api/articles/tags", self.new_data, format="json")
        # add article
        self.article = {
            'title': 'The marriage story',
            'author': 1,
            'tag': [1],
            'description': 'Love is blind',
            'body': 'My wife was a criminal until she met this handsome guy.',
            'read_time': 5
        }
        # tag article
        self.article_data = {
            "tag": [2],
        }
        response = self.client.put(
            "api/articles/1", self.article_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArticleRatingTestCase(ArticleTagsTestCase):
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


class ArticleLikeDisklikeTestCase(ArticleTagsTestCase):
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


class ArticleFavoriteTestCase(ArticleTagsTestCase):
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
