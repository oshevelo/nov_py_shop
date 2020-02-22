from django.test import TestCase
from rest_framework.test import APIClient
from apps.catalogue.models import Category
from rest_framework import status

# Create your tests here.

class CatalogueTestsAPI(TestCase):
    
    def setUp(self):
        self.api = APIClient()
        сat = Category.objects.create(name='test_cat', description='category test')
        cat_2 = Category.objects.create(name='test_cat_2', description='category test 2', parent= сat)

    def tests_category_list(self):
        response = self.api.get('/catalogue/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': 1, 'name': 'test_cat', 'description':'category test',
                'parent':None,'children':[{'id': 2, 'name': 'test_cat_2','description':'category test 2',
                'parent': 1,'children':[],'products':[]}],'products':[]}])
    
        
