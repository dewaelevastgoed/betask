from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from articles.models import Article, Tag
import articles.serializers as ats


class ArticleViewSet(viewsets.ViewSet):
    queryset = Article.objects.all()
    serializer_class = ats.ArticleSerializer
    ordering_fields = ['title', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        title = self.request.query_params.get('title')
        content = self.request.query_params.get('content')
        if title or content is not None:
            try:
                queryset = queryset.filter(Q(title__icontains=title) | Q(content__icontains=content))
                serializer = ats.ArticleSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Article.DoesNotExist:
                return Response(self.serializer_class.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ats.ArticleSerializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            queryset = Article.objects.all()
            article = get_object_or_404(queryset, pk=pk)
            serializer = self.serializer_class(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(self.serializer_class.errors, status=status.HTTP_404_NOT_FOUND)


class TagViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            serializer = ats.TagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = ats.TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        article = Article.objects.get(id=request.data.get('article'))
        tag = Tag.objects.get(id=request.data.get('tag'))
        if tag and article is not None:
            serializer = ats.UpdateArticleTagSerializer(request.data)
            if serializer.is_valid():
                serializer.save(tag=tag)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if article is not None:  # specify an article you want to remove its tag
            serializer = ats.UpdateArticleTagSerializer(request.data)
            if serializer.is_valid():
                serializer.save(tag=None)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, )
    def get_article_by_tag(self, request):
        try:
            article = Article.objects.get(pk=request.data.get('tag_id'))
            if article is not None:
                serializer = ats.ListArticleWithTagsSerializer(article, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response("Article does not exist", status=status.HTTP_404_NOT_FOUND)



