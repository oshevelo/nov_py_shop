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
        fields = ['id', 'pub_id',  'order', 'product', 'amount']
        

class OrderSerializer(serializers.ModelSerializer):

    orderitems=OrderItemBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id',  'pub_id', 'user', 'accepting_time', 'completing_or_rejecting_time', 'status', 'is_paid', 'is_editable', 'max_orderitems', 'comment', 'orderitems']


class OrderItemSerializer(serializers.ModelSerializer):

    product=ProductBriefSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'pub_id',  'order', 'product', 'amount']
        
        
class OrderCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id',  'pub_id', 'accepting_time', 'completing_or_rejecting_time', 'status', 'is_paid', 'comment']
        
        
class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'pub_id', 'product', 'amount']
        
        


