from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from phone_field import PhoneField
import uuid
from django.conf import settings
from apps.carts.models import Cart
from apps.orders.models import Order
from apps.stats.models import Stat


def user_avatar_path(instance, _):
    return 'images/avatars/user_{0}/{1}'.format(
        instance.user.profile.uu_id,
        settings.AVATAR_FILENAME + settings.AVATAR_FILENAME_EXTENSION
    )

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
    avatar = models.ImageField(
        upload_to=user_avatar_path, blank=True, null=True)
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def cart(self):
        return Cart.objects.get(user=self.user)

    @property
    def orders(self):
        return Order.objects.filter(user=self.user)

    @property
    def last_seen_products(self):
        return (Stat.objects
                .filter(user=self.user, action='browse_product')
                .order_by('-created')[:settings.LAST_SEEN_PRODUCTS_COUNT]
                )

    def __str__(self):
        return f'{self.pk}. {self.surname} {self.first_name}'


class UserAddress(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.pk}. {self.address}, {self.city} - {self.user_profile}'


class UserPhone(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='phones',
    )
    phone = PhoneField(help_text='Contact phone number')
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.pk}. {self.phone} - {self.user_profile}'
