from django.db import models
from apps.users.models import UserProfile
from apps.products.models import Product

class Order(models.Model):
    
    user_profile= models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='orders',
    )
   
    accepting_time = models.DateTimeField('Accepting time')
    
    completing_or_rejecting_time = models.DateTimeField('Completing or rejecting time', blank=True, null=True)
    
    status_choices=[
        ('accepted','accepted'),
        ('completed','completed'),
        ('rejected','rejected')
    ]
    status=models.CharField(
        max_length = 20,
        choices=status_choices,
        default='accepted'
    )
    
    comment= models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return 'Order #{} for {}'.format(self.pk, self.user_profile)
        
        
class OrderItem(models.Model):
    
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='orderitems'
    )
    
    product=models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    
    amount = models.IntegerField(default=1)
    
    def __str__(self):
        return '{}, {}  - {} items'.format(self.order, self.product, self.amount)
        
