import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Payment, TransactionLog
from rest_framework import generics
from .serializers import PaymentSerializer
from rest_framework.pagination import LimitOffsetPagination


class PaymentUrl(generics.CreateAPIView):
    '''
        {'order_pub_id': ''}
    '''
    def create(self):
        order_pub_id = self.request.data['order_pub_id']
        payment_system_url = 'https://portmone.com?payeeid={}&order_id={}'.format(settings.payeeid, order_pub_id)
        response = {'payment_system_url': payment_system_url}
        return HttpResponse(json.dumps(response), status=200)


class PaymentSystemCallBack(generics.CreateAPIView):

    def create(self):
        self.request.data#JSON from portmone
        new_log_entry=TransactionLog.objects.create(**{
            'payment': Payment.objects.filter(order_pub_id=self.request.data['ShopOrderNumber']),
	    'status':'new',
            'data': self.request.data
        })
        new_log_entry.process()
        return HttpResponse('OK', status=200)


class PaymentList(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    pagination_class = LimitOffsetPagination


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(Payment, pk=self.kwargs.get('id'))
        return obj
