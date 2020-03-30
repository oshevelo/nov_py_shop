from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile, UserAddress, UserPhone
from apps.carts.serializers import CartSerializer
from apps.products.serializers import ProductSerializer

# Cannot import any serializer from apps.orders.serializers because of a circular import
from apps.orders.models import Order


class OrderBriefSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    pub_id = serializers.CharField()
    accepting_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'pub_id', 'accepting_time', 'status']


class UserBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username']


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

    profile = UserProfileBriefSerializer(read_only=True)

    class Meta:
        model = UserPhone
        fields = ('uu_id', 'phone', 'profile')


class UserAddressSerializer(serializers.ModelSerializer):

    profile = UserProfileBriefSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = ('uu_id', 'city', 'address', 'profile')


class UserProfileSerializer(serializers.ModelSerializer):
    addresses = UserAddressBriefSerializer(many=True, read_only=True)
    phones = UserPhoneBriefSerializer(many=True, read_only=True)
    cart = CartSerializer(read_only=True)
    orders = OrderBriefSerializer(many=True, read_only=True)
    avatar = serializers.ImageField(
        allow_empty_file=True, use_url=True, read_only=True)
    last_seen_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('uu_id', 'first_name', 'surname',
                  'patronymic', 'avatar', 'last_seen_products', 'addresses',
                  'phones', 'cart', 'orders')


class UserAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(allow_empty_file=False)
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    size = serializers.IntegerField()


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = UserAvatarSerializer(required=False, write_only=True)

    class Meta:
        model = UserProfile
        fields = ('uu_id', 'first_name', 'surname',
                  'patronymic', 'avatar')
