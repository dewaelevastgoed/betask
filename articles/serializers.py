from rest_framework import serializers

from articles.models import Article, Tag


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    def perform_delete_on_tag(self):
        tag = self.instance.tag
        if tag:
            self.instance.tag = None
            self.instance.save()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
