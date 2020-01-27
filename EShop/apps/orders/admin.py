from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)


class OrderItemAdmin(admin.ModelAdmin):
    raw_id_fields = ("order",)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
