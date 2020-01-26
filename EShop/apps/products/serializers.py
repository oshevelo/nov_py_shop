from rest_framework import serializers
from .models import Product, Set


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'scu', 'gtin', 'stock', 'is_available')


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('id', 'name', 'description', 'products', 'price')
