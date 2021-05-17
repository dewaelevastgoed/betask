from rest_framework import serializers

from articles.models import Article
from tags.models import Tag


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ('tags', )


class ArticleTagSerializer(serializers.Serializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())
