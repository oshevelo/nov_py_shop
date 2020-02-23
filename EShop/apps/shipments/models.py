import uuid
from django.db import models
from apps.orders.models import Order

# Create your models here.

class Shipment(models.Model):

    HOME_DELIVERY='HOME'
    DROP_POINT='DROP'
    PICK_UP='PICKUP'

    DELIVERY_CHOICES=[
        (HOME_DELIVERY,'Home delivery'),
        (DROP_POINT, 'Drop point'), 
        (PICK_UP, 'Pick up at store'),
    ]

    PACKING=1
    PICKED_UP=2
    IN_TRANSIT=3
    DELIVERED=4
    DELIVERY_STATUS_CHOICES=[
        (PACKING,'Packing'),
        (PICKED_UP, 'Picked up by courier'),
        (IN_TRANSIT, 'In transit'),
        (DELIVERED,'Delivered'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = 'shipments')
    shipment_status = models.IntegerField(choices=DELIVERY_STATUS_CHOICES, default=1)
    shipment_type = models.CharField(
        max_length=50, choices=DELIVERY_CHOICES, default=HOME_DELIVERY
    )
    shipment_date = models.DateField(blank=True, null=True)
    destination_city= models.CharField(max_length=50)
    destination_zip_code = models.IntegerField()
    destination_adress_street = models.CharField(max_length=300)
    destination_adress_building = models.CharField(max_length=5)
    destination_other_details = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.uuid)


