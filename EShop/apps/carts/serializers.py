from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductBriefSerializer


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('cart_uuid', 'user', 'cart_created', 'cart_updated')


class CartBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('cart_uuid', 'cart_updated')


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductBriefSerializer(read_only=True)
    cart = CartBriefSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'price', 'quantity', 'cart_item_created', 'cart_item_updated')


class CartItemBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'cart_item_updated')






