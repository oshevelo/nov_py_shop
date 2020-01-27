from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id',  'order_uuid', 'user', 'accepting_time', 'completing_or_rejecting_time', 'status', 'comment']


class OrderBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'order_uuid', 'user', 'accepting_time', 'status']


class OrderItemSerializer(serializers.ModelSerializer):

    order=OrderBriefSerializer()

    class Meta:
        model = OrderItem
        fields = ['id',  'order', 'product', 'amount']

