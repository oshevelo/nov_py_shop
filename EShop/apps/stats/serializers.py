from rest_framework import serializers
from apps.stats.models import Stat
from apps.users.models import UserProfile
from apps.products.serializers import ProductSerializer


class StatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stat
        fields = ['created', 'action', 'additional_info']


class LastSeenProductsSerializer(serializers.ModelSerializer):

    last_seen_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['last_seen_products']
