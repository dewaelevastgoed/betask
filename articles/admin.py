from django.apps import apps
from django.contrib import admin

for model_class in apps.get_app_config("articles").get_models():
    if not admin.site.is_registered(model_class):
        admin.site.register(model_class)
