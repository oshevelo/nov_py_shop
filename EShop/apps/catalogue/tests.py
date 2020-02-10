from django.test import TestCase
from rest_framework.test import APIClient
from apps.catalogue.models import Category
from rest_framework import status

# Create your tests here.

class CatalogueTestsAPI(TestCase):
    
    def setUp(self):
        сat = Category.objects.create(name='test_cat', description='category test')
        self.c = APIClient()

     def tests_list_category(self):
        c = APIClient()
        response = self.c.get('/catalogue/')
        print(response.status_code)
        print(response.json())

        
    def tests_category(self):
        c = APIClient()
        response = self.c.get('/catalogue/')
        print(response.status_code)
        print(response.json())
        
        

