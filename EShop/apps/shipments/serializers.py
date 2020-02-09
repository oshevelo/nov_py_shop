from rest_framework import serializers
from apps.shipments.models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shipment
        fields = ['id', 'uuid', 'shipment_status', 'shipment_type', 'shipment_date', 'destination_city', 'destination_zip_code', 'destination_adress_street', 'destination_adress_building', 'destination_other_details'
                 ]

