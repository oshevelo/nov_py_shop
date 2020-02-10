from django.db import models
from apps.catalogue.models import SubCategory

class Product(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True)

    price = models.FloatField(default=0)

    scu = models.CharField(max_length=32, help_text='SCU: Stock Keeping Unit')
    gtin = models.CharField(max_length=14, help_text='GTIN: Global Trade Item Number')

    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)

    image = models.ImageField(upload_to='images/', blank=True, null=True)

    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)


class Kit(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True)

    products = models.ManyToManyField(Product)
    discount = models.PositiveIntegerField(default=0, help_text='%%: Percentage discount')

    @property
    def price(self):
        total_price = sum(i[0] for i in self.products.values_list('price'))
        discount_value = self.discount / 100 * total_price
        price = round(total_price - discount_value, 2)

        return price

    def __str__(self):
        return '{} {}'.format(self.id, self.name)
