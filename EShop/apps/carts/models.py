from django.db import models
import datetime
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from apps.products.models import Product


class Cart(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'public_id = {} --- user = {}'.format(self.public_id, self.user)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'public_id = {} --- product = {} --- cart = {}'.format(self.public_id, self.product, self.cart)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

