from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Stat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stats',
    )
    created = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    additional_info = JSONField(blank=True, default=dict)
