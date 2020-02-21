from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import UserProfile, UserAddress, UserPhone
from apps.users.serializers import UserProfileSerializer, UserAddressSerializer, UserPhoneSerializer
from apps.users.permissions import UserProfileEditPermission, RequestIsList

# Create your views here.


class UserProfileList(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(
            UserProfile,
            uu_id=self.kwargs.get('user_profile_uu_id'),
            user=self.request.user)


class UserAddressList(generics.ListCreateAPIView):
    serializer_class = UserAddressSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        (RequestIsList & IsAuthenticated) |
        (UserProfileEditPermission),
    )

    def get_queryset(self):
        return UserAddress.objects.filter(user_profile__user=self.request.user)

    def create(request, *args, **kwargs):
        profile = UserProfile.objects.get(
            uu_id=kwargs['user_profile_uu_id'])
        data = request.request.data
        serializer = request.serializer_class(data=data)
        if serializer.is_valid():
            address = request.request.data['address']
            city = request.request.data['city']
            obj = UserAddress.objects.create(
                city=city, address=address, user_profile=profile)
            response_data = {
                'address': obj.address,
                'city': obj.city,
                # 'uu_id': obj.serializable_value('uu_id'),
            }
            response_serializer = request.serializer_class(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data,
                                status=status.HTTP_201_CREATED)
        return Response(response_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer

    def get_object(self):
        return get_object_or_404(
            UserAddress,
            uu_id=self.kwargs.get('user_address_uu_id'),
            user_profile__user=self.request.user)


class UserPhoneList(generics.ListCreateAPIView):
    serializer_class = UserPhoneSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        (RequestIsList & IsAuthenticated) |
        (UserProfileEditPermission),
    )

    def get_queryset(self):
        return UserPhone.objects.filter(user_profile__user=self.request.user)

    def create(request, *args, **kwargs):
        profile = UserProfile.objects.get(
            uu_id=kwargs['user_profile_uu_id'])
        data = request.request.data
        serializer = request.serializer_class(data=data)
        if serializer.is_valid():
            phone = request.request.data['phone']
            obj = UserPhone.objects.create(
                phone=phone, user_profile=profile)
            response_data = {
                'phone': obj.phone,
                # 'uu_id': obj.serializable_value('uu_id'),
            }
            response_serializer = request.serializer_class(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data,
                                status=status.HTTP_201_CREATED)
        return Response(response_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        # return super(UserPhoneList, request).create(*args, **kwargs)


class UserPhoneDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPhoneSerializer

    def get_object(self):
        return get_object_or_404(
            UserPhone,
            uu_id=self.kwargs.get('user_phone_uu_id'),
            user_profile__user=self.request.user)
