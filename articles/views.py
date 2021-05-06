from rest_framework import generics

from articles.models import Article
from articles.serializers import ArticleSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
