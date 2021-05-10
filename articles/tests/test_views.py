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

    def test_not_found_title_filter(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(f'{reverse("article_list")}?title=xyz')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_not_found_content_filter(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(f'{reverse("article_list")}?content=xyz')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_title_filter(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(f'{reverse("article_list")}?title={article1.title}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), article1.title)

    def test_content_filter(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(
            f'{reverse("article_list")}?content={article1.content}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("content"), article1.content)

    def test_not_found_content_and_title_filter(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(f'{reverse("article_list")}?content=xyz&title=xyz')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_content_and_title_filter(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(
            f'{reverse("article_list")}?content={article1.content}&title={article1.title}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("content"), article1.content)


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
