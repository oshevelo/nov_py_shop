from rest_framework import serializers
from apps.shipments.models import Shipment
from apps.orders.serializers import OrderBriefSerializer

class ShipmentSerializer(serializers.ModelSerializer):

    order = OrderBriefSerializer(read_only=True)    

    class Meta:
        model = Shipment
        fields = ['id', 'uuid', 'order', 'shipment_status', 'shipment_type', 'shipment_date', 'destination_city', 'destination_zip_code', 'destination_adress_street', 'destination_adress_building', 'destination_other_details'
                 ]

