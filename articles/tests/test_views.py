from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from articles.models import Article
from articles.tests.factories import ArticleFactory


class ArticleListCreateAPIViewTest(APITestCase):
    def test_list(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article1.id, article2.id]
        )

    def test_list_filtering(self):
        article1, article2 = ArticleFactory.create_batch(2)
        # filter by title
        response = self.client.get(reverse("article_list"), data={"title": article1.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], article1.id)

        # filter by content
        response = self.client.get(reverse("article_list"), data={"content": article2.content})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], article2.id)

    def test_list_ordering(self):
        article1, article2, article3 = ArticleFactory.create_batch(3)
        # order by title ascending
        response = self.client.get(reverse("article_list"), data={"ordering": 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article1.id, article2.id, article3.id]
        )

        # order by title descending
        response = self.client.get(reverse("article_list"), data={"ordering": '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article3.id, article2.id, article1.id]
        )

        # order by created_at ascending
        response = self.client.get(reverse("article_list"), data={"ordering": 'created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article1.id, article2.id, article3.id]
        )

        # order by created_at descending
        response = self.client.get(reverse("article_list"), data={"ordering": '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article3.id, article2.id, article1.id]
        )

    def test_create(self):
        self.assertEqual(Article.objects.count(), 0)
        data = {
            "title": "Test Article",
            "slug": "test-article",
            "content": "Lorem ipsum",
        }
        response = self.client.post(reverse("article_list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(article.slug, "test-article")


class ArticleDetailAPIViewTest(APITestCase):
    def test_update(self):
        article = ArticleFactory(slug="my-slug")
        data = {"slug": "updated-slug"}
        url = reverse("article_detail", args=(article.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_article = Article.objects.get(id=article.id)
        self.assertEqual(updated_article.slug, "updated-slug")

    def test_delete(self):
        article = ArticleFactory()
        url = reverse("article_detail", args=(article.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)
