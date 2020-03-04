from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(read_only=True, child=RecursiveField())
    
    class Meta:
        model = Category
        fields = ['id','name', 'description', 'parent', 'children', 'products']
