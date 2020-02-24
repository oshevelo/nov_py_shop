from django.contrib import admin
from .models import Category


class CatalogueAdmin(admin.ModelAdmin):
    raw_id_fields = ("category",)


admin.site.register(Category)
