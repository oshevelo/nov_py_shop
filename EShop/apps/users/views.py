from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from apps.users.models import UserProfile, UserAddress, UserPhone
from apps.users.serializers import UserProfileSerializer, UserAddressSerializer, UserPhoneSerializer

# Create your views here.


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = LimitOffsetPagination


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        obj = get_object_or_404(UserProfile, pk=self.kwargs.get('user_profile_id'))
        return obj


class UserAddressList(generics.ListCreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    pagination_class = LimitOffsetPagination


class UserAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer

    def get_object(self):
        obj = get_object_or_404(
            UserAddress, pk=self.kwargs.get('user_address_id'))
        return obj


class UserPhoneList(generics.ListCreateAPIView):
    queryset = UserPhone.objects.all()
    serializer_class = UserPhoneSerializer
    pagination_class = LimitOffsetPagination


class UserPhoneDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPhoneSerializer

    def get_object(self):
        obj = get_object_or_404(UserPhone, pk=self.kwargs.get('user_phone_id'))
        return obj
