# from rest_framework import status
# from django.test import TestCase
# from django.urls import reverse
# from .test_config import MainTestConfig
# from authors.apps.authentication.tests.test_setup import BaseSetUp
# from authors.apps.articles.models import (Article)


# class CreateArticleTestCase(MainTestConfig):
#     def setUp(self):
#         self.base = BaseSetUp()
#         self.client = self.base.client
#         self.article_data = {
#             'title': 'The war storry',
#             'author': 1,
#             'tag': [1],
#             'description': 'Love is blind',
#             'body': 'I really loved war until...',
#             'read_time': 3
#         }
#         self.token = "eSknaojdIdlafesodoilkjIKLLKLJnjudalfdJndajfdaljfeESFdafjdalfjaofje"
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

#     def test_post_article(self):
#         response = self.client.post(
#             reverse('articles'), self.article_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_user_can_get_an_article(self):
#         response = self.client.get(reverse('list', ))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_can_update_article(self):
#         self.client.post(reverse('articles'), self.article_data, format="json")
#         article = Article.objects.get()
#         self.change_article = {'title': 'The love storry'}
#         res = self.client.put(
#             reverse('update', kwargs={'pk': article.id}),
#             self.change_article,
#             format='json')
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_user_can_delete_article(self):
#         self.client.post(reverse('articles'), self.article_data, format="json")
#         article = Article.objects.get()
#         response = self.client.delete(
#             reverse('delete', kwargs={'pk': article.id}),
#             format='json',
#             follow=True)
#         self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


# class CreateCommentTestCase(MainTestConfig):
#     def setUp(self):
#         self.comment_data = {'article': 1, 'user': 1, 'comment': 'Nice story '}

#     def test_user_can_post_a_comment(self):
#         response = self.client.post(
#             reverse('comment'), self.comment_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_user_can_get_all_comments(self):
#         response = self.client.get(reverse('all_comments', ))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class ArticleTagsTestCase(TestCase):
#     """This class defines the api for Tag CRUD methods"""

#     def setUp(self):
#         """"This method sets the test variables and test client"""
#         self.base = BaseSetUp()
#         self.client = self.base.client
#         # Initialize login credentials
#         self.login_data = {
#             "username": "remmy@test.com",
#             "password": "Password123"
#         }
#         # Declare login response
#         self.login_response = self.client.post(
#             "api/users/login", self.login_data, format="json")
#         # Replace the dummy token with self.login_response.data["Token"]
#         self.token = "eSknaojdIdlafesodoilkjIKLLKLJnjudalfdJndajfdaljfeESFdafjdalfjaofje"
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

#     def test_user_can_create_tag(self):
#         """Test user can register new tags"""
#         self.tag_data = {"tag": "Python"}
#         response = self.client.post(
#             "api/articles/tags", self.tag_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_user_can_get_specific_tag(self):
#         """Test api can return specific tag"""
#         response = self.client.get("api/articles/tags/1", format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_can_get_all_tag(self):
#         """Test api can return all tags to enable easy filtering of articles"""
#         response = self.client.get("api/articles/tags", format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_can_update_specific_tag(self):
#         """Test api can update a specific tag"""
#         self.new_data = {"tag": "Love"}
#         response = self.client.put(
#             "api/articles/tags/1", self.new_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_can_delete_specific_tag(self):
#         """Test api can delete specific tag"""
#         response = self.client.get("api/articles/tags/1", format="json")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_user_can_tag_an_article(self):
#         """Test api can add tag to an article"""
#         # add a new tag
#         self.new_data = {"tag": "Marriage"}
#         self.client.post("api/articles/tags", self.new_data, format="json")
#         # add article
#         self.article = {
#             'title': 'The marriage story',
#             'author': 1,
#             'tag': [1],
#             'description': 'Love is blind',
#             'body': 'My wife was a criminal until she met this handsome guy.',
#             'read_time': 5
#         }
#         # tag article
#         self.article_data = {
#             "tag": [2],
#         }
#         response = self.client.put(
#             "api/articles/1", self.article_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class ArticleRatingTestCase(ArticleTagsTestCase):
#     """This class defines the api to article rating test case"""

#     def setUp(self):
#         """Set or initialize the test data"""
#         self.rating = {"article": 1, "author": 1, "rating": 5}

#     def test_user_can_rate_an_article(self):
#         """Test user can rate articles"""
#         # add article
#         self.article = {
#             "title": "The mighty king",
#             "author": 1,
#             "tag": [1],
#             "description": "Killed a lion with a sword",
#             "body": "The JUJU king has done it again...",
#             "read_time": 4
#         }
#         self.client.post("api/articles/", self.article, format="json")
#         # Rate article
#         response = self.client.post(
#             "api/articles/ratings", self.rating, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # Get average ratings average rating for their articles
#         response = self.client.post(
#             "api/articles/user_ratings/1", format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         """ Add the following code when ratings feature is implemented
#             self.assertEqual(response.data['ratings'], 5)
#         """


# class ArticleLikeDisklikeTestCase(ArticleTagsTestCase):
#     """This class defines the api test case to like or dislike articles"""

#     def setUp(self):
#         """Set or initialize the test data"""
#         # add article
#         self.article = {
#             "title": "The killer disease",
#             "author": 1,
#             "tag": [1],
#             "description": "HIV revisited",
#             "body": "Handily did they love him until he was no more...",
#             "read_time": 2
#         }
#         self.like = {"article": 1, "user": 1, "like": True}
#         self.client.post("api/articles", self.article, format="json")
#         response = self.client.post(
#             "api/articles/likes", self.like, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class ArticleFavoriteTestCase(ArticleTagsTestCase):
#     """This class defines the api test case to favorite articles"""

#     def setUp(self):
#         """Set or initialize the test data"""
#         # add article
#         self.article = {
#             "title": "Life Hack Guide",
#             "author": 1,
#             "tag": [1],
#             "description": "Discorer you life in 3 minutes.",
#             "body": "Many people still do not to know what they value in life",
#             "read_time": 3
#         }
#         self.favorite = {"article": 1, "user": 1, "favorite": True}
#         self.client.post("api/articles", self.article, format="json")
#         response = self.client.post(
#             "api/articles/favorites", self.favorite, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
