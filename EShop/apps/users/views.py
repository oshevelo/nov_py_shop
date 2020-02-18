from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from apps.users.models import UserProfile, UserAddress, UserPhone
from apps.users.serializers import UserProfileSerializer, UserAddressSerializer, UserPhoneSerializer

# Create your views here.


class UserProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        obj = get_object_or_404(
            UserProfile, uu_id=self.kwargs.get('user_profile_uu_id'))
        if obj.user == self.request.user:
            return obj
        else:
            raise Http404('No permission')


class UserAddressList(generics.ListCreateAPIView):
    serializer_class = UserAddressSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return UserAddress.objects.filter(user_profile__user=self.request.user)


class UserAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer

    def get_object(self):
        obj = get_object_or_404(
            UserAddress, uu_id=self.kwargs.get('user_address_uu_id'))
        if obj.user_profile.user == self.request.user:
            return obj
        else:
            raise Http404('No permission')


class UserPhoneList(generics.ListCreateAPIView):
    serializer_class = UserPhoneSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return UserPhone.objects.filter(user_profile__user=self.request.user)


class UserPhoneDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPhoneSerializer

    def get_object(self):
        obj = get_object_or_404(
            UserPhone, uu_id=self.kwargs.get('user_phone_uu_id'))
        if obj.user_profile.user == self.request.user:
            return obj
        else:
            raise Http404('No permission')
