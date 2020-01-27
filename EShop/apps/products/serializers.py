from rest_framework import serializers
from .models import Product, Kit


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'scu', 'gtin', 'stock', 'is_available')


class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = ('id', 'name', 'description', 'products', 'price')
