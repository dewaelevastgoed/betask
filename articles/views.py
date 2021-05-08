from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from articles.models import Article, Tag
from articles.serializers import (
    ArticleSerializer,
    TagRemoveOrAddToArticleSerializer,
    TagSerializer,
)


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "content"]
    ordering_fields = ["title", "created_at"]
    search_fields = ["tags__name", "tags__parent__name"]


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def destroy(self, request, *args, **kwargs):
        """Prevent delete if tag is attached to article"""
        instance = self.get_object()
        articles = instance.article_set.exists()
        if articles:
            return Response(
                {"message": "Tag is currently attached to an article"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post", "delete"])
    def add_remove_to_article(self, request):
        """Add API to be able to add/remove Tag(s) to Article(s)."""
        method = request.method.lower()
        serializer = TagRemoveOrAddToArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = Article.objects.get(pk=serializer.validated_data["article_id"])
            tag = Tag.objects.get(pk=serializer.validated_data["tag_id"])
            if method == "post":
                article.tags.add(tag)
                msg = {"status": "Tag added."}
            elif method == "delete":
                article.tags.remove(tag)
                msg = {"status": "Tag removed."}
            return Response(msg)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
