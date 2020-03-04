from django.contrib import admin
from .models import Category


class CatalogueAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('name','parent')
    search_fields = ['name', ]


admin.site.register(Category, CatalogueAdmin)
