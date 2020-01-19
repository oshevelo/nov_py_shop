from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))
