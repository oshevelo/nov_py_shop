from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.


class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        return obj


class CartItemList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        selected_cart = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        return CartItem.objects.filter(cart=selected_cart)
#        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        selected_cart = get_object_or_404(Cart, public_id=self.kwargs.get('cart_uuid'), user=self.request.user)
        obj = get_object_or_404(selected_cart.items , public_id=self.kwargs.get('cart_item_uuid'))
        return obj

