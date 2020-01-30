from rest_framework import serializers
from apps.users.models import UserProfile, UserAddress, UserPhone


class UserProfileBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('uu_id', 'first_name', 'surname')


class UserAddressBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('uu_id', 'city', 'address')


class UserPhoneBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPhone
        fields = ('uu_id', 'phone')


class UserPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPhone
        fields = ('uu_id', 'phone', 'user_profile')


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('uu_id', 'city', 'address', 'user_profile')


class UserProfileSerializer(serializers.ModelSerializer):
    addresses = UserAddressBriefSerializer(many=True)
    phones = UserPhoneBriefSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('uu_id', 'first_name', 'surname',
                  'patronymic', 'user', 'addresses', 'phones')
