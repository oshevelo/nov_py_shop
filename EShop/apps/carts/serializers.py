from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductBriefSerializer


class CartBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('public_id', 'user')


class CartItemBriefSerializer(serializers.ModelSerializer):

    product = ProductBriefSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'public_id', 'product', 'quantity', 'created_at', 'updated_at')


class CartSerializer(serializers.ModelSerializer):

    items = CartItemBriefSerializer(many=True) 

    class Meta:
        model = Cart
        fields = ('id','public_id', 'user', 'created_at', 'updated_at', 'items')

    def create(self, json):
        items_data = json.pop('items')
        cart = Cart.objects.create(**json)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart



class CartItemSerializer(serializers.ModelSerializer):

    product = ProductBriefSerializer(read_only=True)
#    cart = CartBriefSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'public_id', 'cart', 'product', 'price', 'quantity', 'created_at', 'updated_at')


class CartCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id','public_id', 'user', 'created_at', 'updated_at')


class CartItemCreateUpdateSerializer(serializers.ModelSerializer):

    product = ProductBriefSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'public_id', 'cart', 'product', 'price', 'quantity', 'created_at', 'updated_at')
















