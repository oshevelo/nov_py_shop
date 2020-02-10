from rest_framework import serializers
from .models import Category
from .models import SubCategory

class CategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Category
        fields = ['id','name', 'description', 'subcategory']

class SubCategorySerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = SubCategory
        fields = ['id','name', 'description', 'products']
        


