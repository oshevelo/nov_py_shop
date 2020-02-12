from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.products.models import Product


# Create your models here.

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=False)
    date = models.DateTimeField(default=timezone.now, null=True, blank=False)

    def __str__(self):
        return 'user = {}, public_id = {}, date = {}'.format(self.user, self.id, self.date, self.pk)
