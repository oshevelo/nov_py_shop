from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Product, Kit
from .serializers import ProductSerializer, KitSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination


class ProductDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))


class KitsList(generics.ListCreateAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    pagination_class = LimitOffsetPagination


class KitDetail(generics.RetrieveDestroyAPIView):
    serializer_class = KitSerializer

    def get_object(self):
        return get_object_or_404(Kit, pk=self.kwargs.get('kit_id'))
