from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Product, Set
from .serializers import ProductSerializer, SetSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination


class ProductDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))


class SetsList(generics.ListCreateAPIView):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    pagination_class = LimitOffsetPagination


class SetDetail(generics.RetrieveDestroyAPIView):
    serializer_class = SetSerializer

    def get_object(self):
        return get_object_or_404(Set, pk=self.kwargs.get('set_id'))
