from django.contrib import admin
from .models import Shipment

# Register your models here.

class ShipmentAdmin(admin.ModelAdmin):
    raw_id_fields = ("order",)

admin.site.register(Shipment, ShipmentAdmin)
