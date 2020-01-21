from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_create = models.DateTimeField('date created')
    
    def __str__(self):
        return 'pk = {} --- user = {}'.format(self.pk, self.user)

