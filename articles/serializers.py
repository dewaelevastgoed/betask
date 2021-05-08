from rest_framework import serializers

from articles.models import Article, Tag


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def update(self, instance, validated_data):
        """Prevent update of Tag.slug if it has any Article(s) related to it"""
        slug = validated_data.get("slug")
        if slug and slug != instance.slug:
            articles = instance.article_set.all()
            if articles:
                error = {"message": "Tag is currently attached to an article"}
                raise serializers.ValidationError(error)

        instance = super().update(instance, validated_data)
        return instance


class TagRemoveOrAddToArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField()
    tag_id = serializers.IntegerField()

    def validate_article_id(self, value):
        """
        Check that the id exists.
        """
        article = Article.objects.filter(pk=value).exists()
        if not article:
            raise serializers.ValidationError("Invalid article ID")
        return value

    def validate_tag_id(self, value):
        """
        Check that the id exists.
        """
        tag = Tag.objects.filter(pk=value).exists()
        if not tag:
            raise serializers.ValidationError("Invalid tag ID")
        return value
