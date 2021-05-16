from django.db import models

from common.base_model import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    parent = models.OneToOneField(
        "Tag", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
