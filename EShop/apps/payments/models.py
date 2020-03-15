from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.orders.models import Order
from django.contrib.postgres.fields import JSONField


# Create your models here.

status = [
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


class LogsTransaction(models.Model):

    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(max_length=100, choices=status, null=True, blank=False)
    data = JSONField(null=True, blank=False)

    def process(self):
        '''
             VALIDATE json
            self.payment.complited_date = now
            self.order.status = 'payed'
            self.order.save()
            self.payment.save()
            self.status = 'OK'
        '''
