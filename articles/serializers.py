from rest_framework import serializers

from articles.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"

    def update(self, instance, validated_data):
        if instance.article_set.exists() and instance.slug != validated_data["slug"]:
            raise serializers.ValidationError(
                "Cannot update slug because tag has related articles."
            )

        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.parent = validated_data.get("parent", instance.parent)
        instance.save()
        return instance


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleAddRemoveTagsSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Article
        fields = ("tags",)
