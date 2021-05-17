from rest_framework import serializers

from articles.models import Article
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def validate_slug(self, data):
        if self.instance and self.instance.slug != data:
            if Article.objects.filter(tags__id=self.instance.id).exists():
                raise serializers.ValidationError("Article exists with this tag.")
        return data
