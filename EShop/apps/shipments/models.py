from django.db import models

# Create your models here.

class Shipments(models.Model):
    shipment_tracking_number = models.IntegerField()
    #order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    shipment_status = models.IntegerField()
    shipment_type = models.CharField(max_length=50)    
    shipment_date = models.DateField
    destination_city= models.CharField(max_length=50)
    destination_zip_code = models.IntegerField()
    destination_adress_street = models.CharField(max_length=300)
    destination_adress_building = models.CharField(max_length=5)
    destination_other_details = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.shipment_tracking_number)


