from rest_framework import generics, status
from rest_framework.response import Response

from articles.models import Article
from tags.models import Tag
from tags.serializers import TagSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def destroy(self, request, *args, **kwargs):
        tag = self.get_object()
        if Article.objects.filter(tags__id=tag.id).exists():
            return Response({"error": "Article exists with this tag."},
                            status=status.HTTP_400_BAD_REQUEST)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

