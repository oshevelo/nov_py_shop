from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.orders.models import Order
from django.contrib.postgres.fields import JSONField


# Create your models here.

status = [
    ['new', 'new'],
    ['in process', 'in process'],
    ['ready', 'ready']
]


class Payment(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=False)
    creation_date = models.DateTimeField(default=timezone.now, null=True, blank=False)
    complited_date = models.DateTimeField(default=timezone.now, null=True, blank=False)

    def __str__(self):
        return 'user = {}, public_id = {}, complited_date = {}'.format(self.user, self.id, self.complited_date, self.pk)


class TransactionLog(models.Model):

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(max_length=100, choices=status, null=True, blank=False)
    data = JSONField(null=True, blank=False)

    def process(self):
    
        valid_data = self.request.data
        if valid_ser.is_valid():
            self.payment.complited_date = now
            self.order.status_choices = 'completed'
            self.order.save()
            self.payment.save()
            self.status = 'ready'

        
        
        '''
            VALIDATE json
            self.payment.complited_date = now
            self.order.status = 'payed'
            self.order.save()
            self.payment.save()
            self.status = 'OK'
        '''
