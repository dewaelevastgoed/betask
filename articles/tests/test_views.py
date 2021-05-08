from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from articles.models import Article, Tag
from articles.tests.factories import ArticleFactory


class ArticleDetailAPIViewTest(APITestCase):

    def setUp(self):
        self.article_1 = Article.objects.create(
            id=1,
            title="Sample title",
            slug="mu-slug",
            content="Sample content",
            created_at="2020-03-14"
        )
        self.tag_1 = Tag.objects.create(
            slug="my-slug",
            name="slug-name",
        )
        self.tag_2 = Tag.objects.create(
            slug="my-slug",
            name="slug-name",
            parent=self.tag_1
        )
        self.tag_3 = Tag.objects.create(
            slug="my-slug",
            name="slug-name",
            parent=self.tag_2

        )
        self.article_2 = Article.objects.create(
            id=2,
            title="Sample title_2",
            slug="mu-slug_2",
            content="Sample content",
        )
        self.article_3 = Article.objects.create(
            id=3,
            title="Sample title_3",
            slug="mu-slug_3",
            content="Sample content",
        )

    def test_get_article(self):
        response = self.client.get(reverse("article-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # retrieve a single article
        response = self.client.get(reverse("article-detail", kwargs={'pk': "1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
