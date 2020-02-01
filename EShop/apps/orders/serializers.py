from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductBriefSerializer


class OrderBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'pub_id', 'user', 'accepting_time', 'status']
        

class OrderItemBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'pub_id', 'product', 'amount']
        

class OrderSerializer(serializers.ModelSerializer):

    orderitems=OrderItemBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id',  'pub_id', 'user', 'accepting_time', 'completing_or_rejecting_time', 'status', 'comment', 'orderitems']


class OrderItemSerializer(serializers.ModelSerializer):

    order=OrderBriefSerializer(read_only=True)
    product=ProductBriefSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'pub_id',  'order', 'product', 'amount']
        
        


