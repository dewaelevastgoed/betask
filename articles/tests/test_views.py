import random

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

    def test_filtered_article_list_by_title(self):
        # List of Test Article Titles data
        article_titles = ["TestArticle1", "TestArticle2"]

        # Picking up random Article Title from the list
        # For dynamic test
        random_title_index = random.randint(0, len(article_titles) - 1)
        random_title = article_titles[random_title_index]

        # Creating Articles
        for article_title in article_titles:
            ArticleFactory.create(title=article_title)

        # Retreiving Article by filtering with the Random title
        url = reverse("article_list") + f"?title={random_title}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_content = response.json()
        # Checking if Random title is being matched from the Response
        self.assertEqual(len(response_content), 1) and self.assertEqual(
            response_content[0]["title"], random_title
        )

    def test_ordered_article_list(self):
        # List of Test Article Titles data
        article_titles = ["TestArticle1", "TestArticle2"]

        # Creating Articles
        for article_title in article_titles:
            ArticleFactory.create(title=article_title)

        # Picking up random Article Title from the list
        descending_title = article_titles[1]
        url = reverse("article_list") + "?ordering=-title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()

        # Checks if the returned List of items equals to Articles created
        self.assertEqual(len(json_response), len(article_titles))
        self.assertEqual(json_response[0]["title"], descending_title)

    def test_article_not_found_by_title_filter(self):
        response = self.client.get(f'{reverse("article_list")}?title=TestArticle1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
