from django.contrib import admin
from .models import Product, Kit


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'scu', 'gtin', 'stock', 'is_available')
    list_filter = ('is_available',)


class KitAdmin(admin.ModelAdmin):
    raw_id_fields = ('products',)
    list_display = ('id', 'name', 'discount')


admin.site.register(Product, ProductAdmin)
admin.site.register(Kit, KitAdmin)
