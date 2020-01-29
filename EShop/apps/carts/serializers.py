from rest_framework import serializers
from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('cart_uuid',  'user', 'cart_created', 'cart_updated')


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id',  'cart', 'product', 'price', 'quantity', 'cart_item_created', 'cart_item_updated')


