from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True)

    price = models.FloatField(default=0)

    scu = models.CharField(max_length=32, help_text='SCU: Stock Keeping Unit')
    gtin = models.CharField(max_length=14, help_text='GTIN: Global Trade Item Number')

    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)

    image = models.ImageField(upload_to='images/', blank=True, null=True)

    # category = models.ForeignKey(Category)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)


class Kit(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True)

    products = models.ManyToManyField(Product)

    price = models.FloatField(default=0)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)
