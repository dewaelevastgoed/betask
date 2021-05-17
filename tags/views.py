from rest_framework import generics

from tags.models import Tag
from tags.serializers import TagSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

