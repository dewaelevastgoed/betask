from django.db import models

from common.base_model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
