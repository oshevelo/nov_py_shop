from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartCreateUpdateSerializer, CartItemCreateUpdateSerializer

from apps.orders.models import Order, OrderItem
from apps.orders.serializers import OrderSerializer, OrderItemSerializer
import datetime
from django.utils import timezone

# Create your views here.


class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

"""
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartCreateUpdateSerializer
        return CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
"""

class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        return obj

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CartCreateUpdateSerializer
        return CartSerializer


class CartItemList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        selected_cart = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        return CartItem.objects.filter(cart=selected_cart)
#        return CartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateUpdateSerializer
        return CartItemSerializer

    def perform_create(self, serializer):
        selected_cart = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        serializer.save(cart=selected_cart)


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        selected_cart = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        obj = get_object_or_404(selected_cart.items , public_id=self.kwargs.get('cart_item_uuid'))
        return obj

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CartItemCreateUpdateSerializer
        return CartItemSerializer


class Checkout(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        selected_cart = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        new_order = Order.objects.create(user=self.request.user, accepting_time=timezone.now())
        for item in selected_cart.items.all():
            order_item = OrderItem.objects.create(order=new_order, product=item.product)
        return new_order     
#        return redirect(reverse('orders:order_details', kwargs={'order_uuid': new_order.pub_id})) 


