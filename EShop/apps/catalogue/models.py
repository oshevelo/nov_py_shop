from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=200, blank=False, unique=True)
    description = models.TextField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')    

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return '{}'.format(self.name)


