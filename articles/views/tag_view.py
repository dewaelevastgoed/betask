from rest_framework import generics

from articles.models import Tag
from articles.serializers import TagSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
