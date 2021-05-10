from rest_framework import generics, status
from rest_framework.response import Response

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

    def destroy(self, request, pk):
        # Note the use of `get_queryset()` instead of `self.queryset`
        remove_tag = request.query_params.get("removeTag")
        instance = self.get_object()

        try:
            if remove_tag and self.validate_remove_tag(remove_tag=remove_tag):
                self.serializer_class(instance=instance).perform_delete_on_tag()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as error:
            return Response(
                data=dict(error=str(error)), status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def validate_remove_tag(self, remove_tag):
        if remove_tag.lower() != "true":
            raise ValueError("specify 'removeTag' to be true")
        return True


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
