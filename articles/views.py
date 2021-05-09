from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.db.models import Q

from articles.models import Article, Tag
from articles.serializers import (
    ArticleAddRemoveTagsSerializer,
    ArticleSerializer,
    TagSerializer,
)


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["title", "created_at"]
    filterset_fields = ["title", "content"]


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleAddRemoveTagAPIView(generics.GenericAPIView):
    serializer_class = ArticleAddRemoveTagsSerializer

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleAddRemoveTagsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags = serializer.validated_data["tags"]
        article.tags.add(*tags)

        return Response(status.HTTP_200_OK)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleAddRemoveTagsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags = serializer.validated_data["tags"]
        article.tags.remove(*tags)

        return Response(status.HTTP_200_OK)


class ArticleListByTagsAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        tag_id = self.kwargs.pop("tag_id", None)
        return Article.objects.filter(Q(tags__id=tag_id) | Q(tags__parent__id=tag_id))


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        tag = get_object_or_404(Tag, pk=pk)
        if tag.article_set.exists():
            return Response(
                "Cannot delete slug because tag has related articles.",
                status.HTTP_400_BAD_REQUEST,
            )

        tag.delete()

        return Response(status.HTTP_200_OK)
