from rest_framework import serializers
from .models import Payment, TransactionLog
from apps.orders.serializers import OrderBriefSerializer


class PaymentSerializer(serializers.ModelSerializer):
    
    order = OrderBriefSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'order', 'creation_date', 'complited_date']
