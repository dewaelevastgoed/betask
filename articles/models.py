from django.db import models


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    parent = models.ForeignKey("Tag", on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField()
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"name:<{self.name}>-slug<{self.slug}>"
