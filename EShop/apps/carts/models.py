from django.db import models
import datetime
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from apps.products.models import Product


class Cart(models.Model):
    cart_uuid = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    cart_created = models.DateTimeField(auto_now_add=True)
    cart_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'cart_uuid = {} --- user = {}'.format(self.cart_uuid, self.user)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    cart_item_created = models.DateTimeField(auto_now_add=True)
    cart_item_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'pk = {} --- product = {} --- cart = {}'.format(self.pk, self.product, self.cart)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

