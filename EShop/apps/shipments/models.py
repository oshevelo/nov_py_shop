import uuid
from django.db import models
from apps.orders.models import Order
from django.contrib.postgres.fields import JSONField


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
    shipment_tracking_number=models.IntegerField()
    shipment_COD=models.Boolean()
    #shipment_system_id = models.CharField(max_length=25) номер накладной из портмоне
    #payment_done = True|false

    def __str__(self):
        return '{} - {}'.format(self.id, self.uuid)

    def send_to_novapochta(self):
        '''
            1. connect to portmone api
            2. save to log what is going to send
            3. save novapochta reply
            4. process_log()
        '''
        client=NovaPoshtaApi(api_key='')
                
        
    class ShipmentTransactionLog(models.Model):
    
    shipment=models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True, blank=False, related_name='shipment_reference')
    request_time=models.DateTimeField(auto_add_now=True)    
    request_payload=JSONField()
    response_payload=JSONField()
    is_error=models.Boolean()
        

    
