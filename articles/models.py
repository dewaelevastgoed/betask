from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()
    tag = models.ForeignKey("Tag", on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    parent = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True)
    slug = models.SlugField()
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

