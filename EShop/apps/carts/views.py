from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = LimitOffsetPagination


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        obj = get_object_or_404(Cart, cart_uuid=self.kwargs.get('cart_uuid'))
        return obj


class CartItemList(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = LimitOffsetPagination


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_object(self):
        obj = get_object_or_404(CartItem, pk=self.kwargs.get('cart_item_id'))
        return obj

