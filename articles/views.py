from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from articles.filters import ArticleFilter
from articles.models import Article
from articles.serializers import ArticleSerializer, ArticleTagSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ArticleFilter
    ordering_fields = ('title', 'created_at')


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleTagCreateAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleTagSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = serializer.validated_data["article"]
        tag = serializer.validated_data["tag"]
        article.tags.add(tag)
        return Response({}, status=status.HTTP_201_CREATED)


class ArticleTagDestroyAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleTagSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = serializer.validated_data["article"]
        tag = serializer.validated_data["tag"]
        article.tags.remove(tag)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
