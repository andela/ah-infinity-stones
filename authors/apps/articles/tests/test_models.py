from django.test import TestCase
from authors.apps.articles.models import (
    Article, FavoriteArticle, Comment, LikesDislike,
    ArticleRating, Tag, BookmarkedArticle, Report,
    Highlight, CommentHistory
)


class ModelTestCase(TestCase):
    """This class defines the test suit for the artile models"""

    def setUp(self):
        """This method defines the test client and other test variables"""

        # Define test variables for articles model
        self.article_title = "The joy of love"
        self.article = Article(title=self.article_title)

        # Define test variables for favorite article model
        self.favorite_article = True
        self.favorites = FavoriteArticle(favorite=self.favorite_article)

        # Define test variables for article comments model
        self.article_comment = "This is awesome..."
        self.comments = Comment(comment=self.article_comment)

        # Define test variables for article likes and dislikes model
        self.article_like = True
        self.likes = LikesDislike(like=self.article_like)

        # Define test variables for Article Ratings model
        self.rate_id = 5
        self.article_ratings = ArticleRating(rating=self.rate_id)

        # Define test variables Article Tags model
        self.tag_name = "Love"
        self.tags = Tag(tag=self.tag_name)

        # Define test variables for Bookmarked Articles model
        self.bookmark = True
        self.bookmarks = BookmarkedArticle(bookmarked=self.bookmark)

        # Define test variables for Report model
        self.report = "This story is plagiarised"
        self.reports = Report(message=self.report)

        # Define test variables for Article Highlights
        self.article_section = "I really regreted having lost him"
        self.sections = Highlight(section=self.article_section)

        # Define test variables for Comment History
        self.comment = "I really regreted having lost her"
        self.history = CommentHistory(new_comment=self.comment)

    def test_article_model_can_be_created(self):
        """Test the model can create Article table"""
        first_count = Article.objects.count()
        self.article.save()
        last_count = Article.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_favorite_article_model_can_be_created(self):
        """Test the model can create Favorite Article table"""
        first_count = FavoriteArticle.objects.count()
        self.favorites.save()
        last_count = FavoriteArticle.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_comments_model_can_be_created(self):
        """Test the model can create Comment table"""
        first_count = Comment.objects.count()
        self.comments.save()
        last_count = Comment.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_article_likes_model_can_be_created(self):
        """Test the model can create Article likes table"""
        first_count = LikesDislike.objects.count()
        self.likes.save()
        last_count = LikesDislike.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_article_ratings_model_can_be_created(self):
        """Test the model can create Article Rating table"""
        first_count = ArticleRating.objects.count()
        self.article_ratings.save()
        last_count = ArticleRating.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_tag_model_can_be_created(self):
        """Test the model can create Tag table"""
        first_count = Tag.objects.count()
        self.tags.save()
        last_count = Tag.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_article_bookmarks_model_can_be_created(self):
        """Test the model can create Article Bookmarks table"""
        first_count = BookmarkedArticle.objects.count()
        self.bookmarks.save()
        last_count = BookmarkedArticle.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_article_report_model_can_be_created(self):
        """Test the model can create Report table"""
        first_count = Report.objects.count()
        self.reports.save()
        last_count = Report.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_article_highlights_model_can_be_created(self):
        """Test the model can create Article Highlights table"""
        first_count = Highlight.objects.count()
        self.sections.save()
        last_count = Highlight.objects.count()
        self.assertNotEqual(first_count, last_count)

    def test_comment_history_model_can_be_created(self):
        """Test the model can create Comment History table"""
        first_count = CommentHistory.objects.count()
        self.history.save()
        last_count = CommentHistory.objects.count()
        self.assertNotEqual(first_count, last_count)
