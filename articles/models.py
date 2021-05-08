from django.db import models


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField("tag", blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
