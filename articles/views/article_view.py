from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from articles.models import Article
from articles.serializers import ArticleSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    # Orders the list based on the following fields
    # Passed from Query-Params
    ordering_fields = ["title", "created_at"]
    filterset_fields = ["title", "content"]
    search_fields = ["tags__name", "tags__parent__name"]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
