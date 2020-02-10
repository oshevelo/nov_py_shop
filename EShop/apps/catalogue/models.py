from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
        
    def __str__(self):
        return '{}'.format(self.name)

    
class SubCategory(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    parent_cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory', null=True)

    def __str__(self):
        return '{}'.format(self.name)
