from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from articles.models import Article, Tag
from articles.tests.factories import ArticleFactory, TagFactory


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

    def test_filtering(self):
        """Test Filtering"""
        articles = ArticleFactory.create_batch(3)
        response = self.client.get(reverse("article_list") + "?title=Article 3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Article 3")

    def test_ordering(self):
        """Test ordering"""
        articles = ArticleFactory.create_batch(5)
        # ascending
        response = self.client.get(reverse("article_list") + "?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sorted_articles = sorted(articles, key=lambda x: x.title)
        self.assertEqual(
            [article["id"] for article in response.data],
            [article.id for article in sorted_articles],
        )
        # descending
        response = self.client.get(reverse("article_list") + "?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sorted_articles = sorted(articles, key=lambda x: x.title, reverse=True)
        self.assertEqual(
            [article["id"] for article in response.data],
            [article.id for article in sorted_articles],
        )


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


class TagViewsetTest(APITestCase):
    def test_list(self):
        tag1, tag2 = TagFactory.create_batch(2)
        response = self.client.get("/api/tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([tag["id"] for tag in response.data], [tag1.id, tag2.id])

    def test_create(self):
        self.assertEqual(Tag.objects.count(), 0)
        data = {
            "name": "Test Tag",
            "slug": "test-tag",
        }
        response = self.client.post("/api/tags/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag = Tag.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(tag.slug, "test-tag")
