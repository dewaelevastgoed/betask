from rest_framework import generics

from django.db.models import Q

from articles.models import Article, Tag
from articles.serializers import ArticleSerializer, TagSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        """
        added params filter for 'title' and 'content'
        """
        title = self.request.query_params.get("title")
        content = self.request.query_params.get("content")

        if title is not None and content is None:
            queryset = self.queryset.filter(title__exact=title)
            return queryset
        elif content is not None and title is None:
            queryset = self.queryset.filter(content__exact=content)
            return queryset
        elif content and title:
            queryset = self.queryset.filter(
                Q(content__exact=content) & Q(title__exact=title)
            )
            return queryset

        return self.queryset.all()


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
