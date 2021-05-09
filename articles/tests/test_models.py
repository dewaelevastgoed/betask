from django.test import TestCase

from articles.tests.factories import ArticleFactory, TagFactory


class ArticleTest(TestCase):
    def test_str(self):
        article = ArticleFactory(title="Test Title")
        self.assertEqual(str(article), "Test Title")


class TagTest(TestCase):
    def test_str(self):
        tag = TagFactory(name="Test Name")
        self.assertEqual(str(tag), "Test Name")
