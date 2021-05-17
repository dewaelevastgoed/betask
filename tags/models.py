from django.db import models


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey('tags.Tag', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
