from rest_framework import serializers
from apps.users.models import UserProfile, UserAddress, UserPhone


class UserProfileBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'surname')


class UserAddressBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('id', 'city', 'address')


class UserPhoneBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPhone
        fields = ('id', 'phone')


class UserPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPhone
        fields = ('id', 'phone', 'user')


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('id', 'city', 'address', 'user')


class UserProfileSerializer(serializers.ModelSerializer):
    addresses = UserAddressSerializer(many=True)
    phones = UserPhoneSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'surname',
                  'patronymic', 'user', 'addresses', 'phones')
