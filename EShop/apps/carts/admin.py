from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)


class CartItemAdmin(admin.ModelAdmin):
    raw_id_fields = ("cart",)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
