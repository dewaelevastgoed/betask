import factory

from articles.models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Article {n}")
    slug = factory.Sequence(lambda n: f"article-{n}")
    content = factory.Sequence(lambda n: f"body {n}")

    class Meta:
        model = Article
