from django.shortcuts import render, get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys
from django.conf import settings
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import UserProfile, UserAddress, UserPhone
from apps.users.serializers import (
    UserProfileSerializer, UserAddressSerializer,
    UserPhoneSerializer, UserProfileUpdateSerializer)
from apps.users.permissions import UserProfileEditPermission, RequestIsList
from apps.carts.models import Cart
from apps.orders.models import Order


# Create your views here.


class UserProfileList(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cart = Cart.objects.get(user=request.user)
        instance.orders = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if 'avatar' in serializer.validated_data:
            image = Image.open(serializer.validated_data['avatar']['avatar'])
            filename = serializer.validated_data['avatar']['avatar'].name
            origin_width, origin_height = image.size
            left = serializer.validated_data['avatar']['x']
            upper = serializer.validated_data['avatar']['y']
            size = min(
                serializer.validated_data['avatar']['size'],
                origin_width - left,
                origin_height - upper,
            )
            right = size + left
            lower = size + upper
            image = image.crop((left, upper, right, lower))
            image = image.resize(
                size=(settings.AVATAR_SIZE, settings.AVATAR_SIZE)
            )
            output = BytesIO()
            image.save(output,
                       format=settings.AVATAR_PIL_FORMAT,
                       quality=settings.AVATAR_QUALITY)
            output.seek(0)
            cropped_image_file = InMemoryUploadedFile(
                output, 'ImageField',
                filename,
                settings.AVATAR_FILE_FORMAT,
                sys.getsizeof(output),
                None)
            serializer.validated_data['avatar'] = cropped_image_file
        serializer.save()

    def get_object(self):
        return get_object_or_404(
            UserProfile,
            uu_id=self.kwargs.get('user_profile_uu_id'),
            user=self.request.user)


class UserAddressList(generics.ListCreateAPIView):
    serializer_class = UserAddressSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticated & (
            RequestIsList | UserProfileEditPermission
        ),
    )

    def get_queryset(self):
        return UserAddress.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user_profile=profile)


class UserAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            UserAddress,
            uu_id=self.kwargs.get('user_address_uu_id'),
            user_profile__user=self.request.user)


class UserPhoneList(generics.ListCreateAPIView):
    serializer_class = UserPhoneSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticated & (
            RequestIsList | UserProfileEditPermission
        ),
    )

    def get_queryset(self):
        return UserPhone.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user_profile=profile)


class UserPhoneDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPhoneSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            UserPhone,
            uu_id=self.kwargs.get('user_phone_uu_id'),
            user_profile__user=self.request.user)
