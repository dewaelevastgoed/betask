from django.contrib import admin

from articles.models import Article,Tag

admin.site.register(Article)
admin.site.register(Tag)
