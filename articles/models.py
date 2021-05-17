from django.db import models


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField('tags.Tag')

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
