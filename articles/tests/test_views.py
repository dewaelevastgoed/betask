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

    def test_filtered_list(self):
        ArticleFactory.create(title="A article")
        ArticleFactory.create(title="B article")
        url = reverse("article_list") + f"?title={'A article'}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]["title"], "A article")

    def test_ordered_list(self):
        ArticleFactory.create(title="A article")
        ArticleFactory.create(title="B article")
        url = reverse("article_list") + "?ordering=-title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["title"], "B article")

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


class ArticleAddRemoveTagAPIViewTest(APITestCase):
    def test_add_tags(self):
        article = ArticleFactory()
        self.assertFalse(article.tags.exists())
        tag = TagFactory()
        data = {
            "tags": [
                tag.id,
            ]
        }
        add_tag_response = self.client.post(
            reverse("article_add_remove_tags", args=(article.id,)), data=data
        )
        self.assertEqual(add_tag_response.status_code, status.HTTP_200_OK)
        self.assertTrue(article.tags.exists())
        self.assertEqual(len(list(article.tags.all())), 1)

    def test_remove_tags(self):
        article = ArticleFactory()
        self.assertFalse(article.tags.exists())
        tag = TagFactory()
        article.tags.add(tag)
        data = {
            "tags": [
                tag.id,
            ]
        }
        self.assertTrue(article.tags.exists())
        self.assertEqual(len(list(article.tags.all())), 1)

        remove_tag_response = self.client.delete(
            reverse("article_add_remove_tags", args=(article.id,)), data=data
        )
        self.assertEqual(remove_tag_response.status_code, status.HTTP_200_OK)
        self.assertFalse(article.tags.exists())


class ArticleListByTagsAPIViewTest(APITestCase):
    def test_list_by_tags(self):
        article1, article2 = ArticleFactory.create_batch(2)
        (
            tag1,
            tag2,
        ) = TagFactory.create_batch(2)
        tag3 = TagFactory(parent=tag1)
        article1.tags.add(tag3)
        article2.tags.add(tag2)
        response = self.client.get(reverse("article_list_by_tag", args=(tag1.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]["id"], article1.id)


class TagListCreateAPIViewTest(APITestCase):
    def test_list(self):
        tag1, tag2 = TagFactory.create_batch(2)
        response = self.client.get(reverse("tag_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([tag["id"] for tag in response.data], [tag1.id, tag2.id])

    def test_create(self):
        self.assertEqual(Tag.objects.count(), 0)
        data = {
            "name": "Test Tag",
            "slug": "test-tag",
            "parent": "",
        }
        response = self.client.post(reverse("tag_list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag = Tag.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(tag.slug, "test-tag")


class TagDetailAPIViewTest(APITestCase):
    def test_update_fail(self):
        article = ArticleFactory.create(title="A article")
        tag = TagFactory(slug="my-slug")
        article.tags.add(tag)
        data = {"slug": "updated-slug"}
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_success(self):
        tag = TagFactory(slug="my-slug")
        data = {"slug": "new-updated-slug"}
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tag = Tag.objects.get(id=tag.id)
        self.assertEqual(updated_tag.slug, "new-updated-slug")

    def test_delete_fail(self):
        article = ArticleFactory.create(title="A article")
        tag = TagFactory(slug="my-slug")
        article.tags.add(tag)
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success(self):
        tag = TagFactory(slug="my-slug")
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deleted_tag = Tag.objects.filter(id=tag.id).first()
        self.assertIsNone(deleted_tag)
