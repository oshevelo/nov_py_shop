from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id',  'pub_id', 'user', 'accepting_time', 'completing_or_rejecting_time', 'status', 'comment']


class OrderBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'pub_id', 'user', 'accepting_time', 'status']


class OrderItemSerializer(serializers.ModelSerializer):

    order=OrderBriefSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'pub_id',  'order', 'product', 'amount']

