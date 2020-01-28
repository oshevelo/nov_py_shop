from rest_framework import serializers
from .models import Product, Kit


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price')


class KitSerializer(serializers.ModelSerializer):
    products = ProductBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Kit
        fields = ('id', 'name', 'description', 'products', 'discount', 'price')
