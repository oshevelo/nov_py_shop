from rest_framework import serializers
from apps.stats.models import Stat


class StatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stat
        fields = ['created', 'action', 'additional_info']
