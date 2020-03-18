from rest_framework import serializers
from apps.shipments.models import Shipment
from apps.orders.serializers import OrderBriefSerializer
from apps.orders.models import Order


class ShipmentSerializer(serializers.ModelSerializer):

    order = OrderBriefSerializer()    


    class Meta:
        model = Shipment
        fields = ['uuid', 'order', 'shipment_status', 'shipment_type', 'shipment_date', 'destination_city', 'destination_zip_code', 'destination_adress_street', 'destination_adress_building', 'destination_other_details'
                 ]

    def validate_order(self, value):
        order = Order.objects.filter(id=value['id']).first()
        if not order:
            raise serializers.ValidationError("bad order id")
        elif not order.is_editable:                   
            raise serializers.ValidationError("no new shipment allowed for paid order")
        return value 

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        order = Order.objects.filter(id=order_data['id']).first()
        validated_data.update({'order': order})
        shipment = Shipment.objects.create(**validated_data)
        return shipment
    
