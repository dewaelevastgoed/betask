from rest_framework import serializers

from articles.models import Article, Tag


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Article
        fields = "__all__"
