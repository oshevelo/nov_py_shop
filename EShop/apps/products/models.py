from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True)

    price = models.FloatField(default=0)

    scu = models.CharField(max_length=32) # Stock Keeping Unit, SCU
    gtin = models.CharField(max_length=14)  # Global Trade Item Number, GTIN

    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)

    # image = models.ImageField()

    # category = models.ForeignKey(Category)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)
