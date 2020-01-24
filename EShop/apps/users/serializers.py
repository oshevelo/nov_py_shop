from rest_framework import serializers
from apps.users.models import UserProfile, UserAddress, UserPhone


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'surname', 'patronymic', 'user')


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('id', 'city', 'address', 'user')


class UserPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPhone
        fields = ('id', 'phone', 'user')
