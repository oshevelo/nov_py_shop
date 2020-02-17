from .models import Order, OrderItem
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderItemSerializer, OrderCreateUpdateSerializer, OrderItemCreateUpdateSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404


class OrderList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateUpdateSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'))
        if obj.user==self.request.user:
            return obj
        else:
            raise Http404()
            
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderCreateUpdateSerializer
        return OrderSerializer
        

class OrderItemList(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer
    
    def get_queryset(self):
        selected_order = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'))
        if selected_order.user!=self.request.user:
            raise Http404()
        return OrderItem.objects.filter(order=selected_order)
        
    def perform_create(self, serializer):
        selected_order=Order.objects.get(pub_id=self.kwargs['order_uuid'])
        serializer.save(order=selected_order)


class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer

    def get_object(self):
        selected_order = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'))
        if selected_order.user!=self.request.user:
            raise Http404()
        obj = get_object_or_404(selected_order.orderitems, pub_id=self.kwargs.get('orderitem_uuid'))
        return obj
