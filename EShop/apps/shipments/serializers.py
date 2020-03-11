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
            raise serializers.ValidationError("bae order id")
        return value 
        # todo: remove after relations feature release
    #    profile = Profile.objects.filter(id=value).first()
     #   if profile is None or (profile is not None and profile.allowed_relations is False):
    # #       raise serializers.ValidationError("Profile is not allowed to add to relations")
     #   return value

    def create(self, validated_data):
        print('in create')
        print(validated_data)
        order_data = validated_data.pop('order')
        order = Order.objects.filter(id=order_data['id']).first()
        validated_data.update({'order': order})
        shipment = Shipment.objects.create(**validated_data)
        return shipment
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
