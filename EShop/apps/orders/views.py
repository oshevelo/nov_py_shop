from .models import Order, OrderItem
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .serializers import OrderSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        obj = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'))
        return obj
        

class OrderItemList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = LimitOffsetPagination


class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer

    def get_object(self):
        obj = get_object_or_404(OrderItem, pk=self.kwargs.get('orderitem_id'))
        return obj
