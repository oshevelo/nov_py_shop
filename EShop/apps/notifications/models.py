from django.db import models
from django.contrib.auth.models import User


class Notificator(models.Model):
    choice = [
        ('one', 'SMS'),
        ('two', 'Viber'),
        ('three', 'Mail'),
        ('four', 'Telegram'),
    ]
    notification_who = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_how = models.CharField(max_length=20, choices=choice, default='three')
    notification_title = models.CharField(max_length=100, null=None)
    notification_what = models.TextField(max_length=255)
    notification_date = models.DateTimeField('date published')
