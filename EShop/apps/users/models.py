from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


# Create your models here.
class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )


class UserAddress(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)


class UserPhone(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    phone = PhoneField(help_text='Contact phone number')
