from rest_framework import serializers
from apps.shipments.models import Shipment
from apps.orders.serializers import OrderBriefSerializer

class ShipmentSerializer(serializers.ModelSerializer):

    order = OrderBriefSerializer(read_only=True)    

    class Meta:
        model = Shipment
        fields = ['id', 'uuid', 'order_id', 'order', 'shipment_status', 'shipment_type', 'shipment_date', 'destination_city', 'destination_zip_code', 'destination_adress_street', 'destination_adress_building', 'destination_other_details'
                 ]

    '''
        perform_create
            1) order_data = json.pop['order']
            2) shipment = Shipment(**json)
            3) order_obj = Order.objects.filter(id=order_data['id']).first()
            4) shipment.order = order_obj
            5) shipment.save()
        
        to optimize
            1) extra Serializer for POST
            2) perform_create
                1) order_data = json.pop['order']
                2) json.update({'order':  Order.objects.filter(id=order_data['id']).first()})
                3) shipment = Shipment.objects.create(**json)


        class OrderField(serializers.Field):
            def to_internal_value(self, data):
                retrun Order.objects.filter(id=data['id']).first()
    '''
