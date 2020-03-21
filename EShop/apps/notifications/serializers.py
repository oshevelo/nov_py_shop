from rest_framework import serializers, viewsets
from .models import Notificator


class NotificatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificator
        fields = [
            'notification_how',
            'notification_title',
            'notification_what',
            'notification_date',
            'notification_who',
        ]


class NotificatorViewSet(viewsets.ModelViewSet):
    queryset = Notificator.objects.all()
    serializer_class = NotificatorSerializer
