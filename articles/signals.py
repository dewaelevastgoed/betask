from rest_framework.exceptions import NotAcceptable

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from articles.models import Article, Tag


@receiver(pre_delete, sender=Tag)
def check_tag_before_del(sender, instance, using, **kwargs):
    tag_present = Article.objects.filter(tag_id=instance.id)
    if tag_present:
        raise NotAcceptable(detail="This tag is used by article", code=400)


@receiver(pre_save, sender=Tag)
def check_tag_before_del(sender, instance, using, update_fields, **kwargs):
    tag_present = Article.objects.filter(tag_id=instance.id)
    if tag_present:
        updated_slug = instance.slug
        previous_slug = tag_present[0].slug
        if updated_slug != previous_slug:
            raise NotAcceptable(
                detail="This tag is used by article and 'slug' cannot be updated",
                code=400,
            )
