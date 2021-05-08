from django.conf.urls import include
from django.urls import path

from rest_framework import routers
from rest_framework.routers import DefaultRouter
import articles.views as av

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register('article', av.ArticleViewSet, 'article')
app_router.register('tag', av.TagViewSet, 'tag')


urlpatterns = [

    path('', include(app_router.urls)),

]
