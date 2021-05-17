from django.db.models import Q
from django_filters.rest_framework import FilterSet

from articles.models import Article


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ('title', 'content', )

    @property
    def qs(self):
        qs = super().qs
        tag = self.request.query_params.get('tag')
        if tag is not None:
            qs = qs.filter(Q(tags__id=tag) | Q(tags__parent__id=tag))
        return qs
