from .models import Order, OrderItem
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .serializers import OrderSerializer, OrderItemSerializer, OrderItemBriefSerializer
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
    pagination_class = LimitOffsetPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderItemBriefSerializer
        return OrderItemSerializer


class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderItemBriefSerializer
        return OrderItemSerializer

    def get_object(self):
        obj = get_object_or_404(OrderItem, pub_id=self.kwargs.get('orderitem_uuid'))
        return obj
