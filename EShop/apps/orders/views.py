from .models import Order, OrderItem
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderItemSerializer, OrderCreateUpdateSerializer, OrderItemCreateUpdateSerializer, ShipmentCreateSerializer
from django.shortcuts import get_object_or_404
from .permissions import OrderEditPermission, AddOrderItemPermission, ReadOnlyMethod, ShipmentExists


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
    permission_classes = [IsAuthenticated&(ReadOnlyMethod|OrderEditPermission)]

    def get_object(self):
        obj = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'), user=self.request.user)
        return obj
            
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderCreateUpdateSerializer
        return OrderSerializer
        

class OrderItemList(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated&(ReadOnlyMethod|OrderEditPermission)&AddOrderItemPermission]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer
    
    def get_queryset(self):
        selected_order = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'), user=self.request.user)
        return OrderItem.objects.filter(order=selected_order)
        
    def perform_create(self, serializer):
        selected_order=get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'), user=self.request.user)
        serializer.save(order=selected_order)


class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated&(ReadOnlyMethod|OrderEditPermission)]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer

    def get_object(self):
        selected_order = get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'), user=self.request.user)
        obj = get_object_or_404(selected_order.orderitems, pub_id=self.kwargs.get('orderitem_uuid'))
        return obj
        
        
class CreateShipment(generics.CreateAPIView):
        permission_classes = [IsAuthenticated&ShipmentExists]
        serializer_class = ShipmentCreateSerializer
        
        def perform_create(self, serializer):
            selected_order=get_object_or_404(Order, pub_id=self.kwargs.get('order_uuid'), user=self.request.user)
            serializer.save(order=selected_order)        