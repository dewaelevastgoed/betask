from rest_framework import serializers

from articles.models import Tag


class TagSerializer(serializers.ModelSerializer):
    def __update_instance_values(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.parent = validated_data.get("parent", instance.parent)
        return instance

    def update(self, instance, validated_data):
        # Checks If there is an Article with tags attached
        # And if the updating slug is different when being assigned to
        # an Article will raise an Error
        if instance.article_set.exists() and instance.slug != validated_data["slug"]:
            raise serializers.ValidationError(
                "Update failed as Slug of Tag is being used by Article(s)"
            )
        instance = self.__update_instance_values(instance, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Tag
        fields = "__all__"
