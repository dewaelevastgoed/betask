from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from articles.models import Tag
from articles.serializers import TagSerializer
from common.base_view import BaseView


class TagListCreateAPIView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailAPIView(RetrieveUpdateDestroyAPIView, BaseView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def destroy(self, request, pk):
        tag_instance = self.get_object()
        if tag_instance.article_set.exists():
            return self.bad_request_response(
                "Operation not permitted, Tag is assigned to an Article"
            )
        self.perform_destroy(tag_instance)
        return self.resource_deleted_response("Tag deleted successfully")
