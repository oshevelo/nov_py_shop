from django.test import TestCase
from rest_framework.test import APIClient
from apps.catalogue.models import Category
from apps.catalogue.models import SubCategory
from rest_framework import status

# Create your tests here.

class CatalogueTestsAPI(TestCase):
    
    def setUp(self):
        self.api = APIClient()
        сat = Category.objects.create(name='test_cat', description='category test')
        cat_2 = Category.objects.create(name='test_cat_2', description='category test 2')
        sub_cat = SubCategory.objects.create(name='test_subcat', description='subcategory test')
        sub_cat_2 = SubCategory.objects.create(name='test_subcat_2', description='subcategory test 2')
        

    def tests_category_list(self):
        response = self.api.get('/catalogue/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': 1, 'name': 'test_cat', 'description':'category test', 'subcategory':[]},
                                           {'id': 2, 'name': 'test_cat_2', 'description':'category test 2', 'subcategory':[]}]
                         )
    def tests_subcategory_list(self):
        response = self.api.get('/catalogue/subcategory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': 3, 'name': 'test_subcat', 'description':'subcategory test', 'products':[]},
                                           {'id': 4, 'name': 'test_subcat_2', 'description':'subcategory test 2', 'products':[]}]
                         )

        
