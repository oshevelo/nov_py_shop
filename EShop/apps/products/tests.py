from django.test import TestCase
from rest_framework.test import APIClient
from apps.products.models import Product
from rest_framework import status


class ProductsTestAPI(TestCase):
    def setUp(self):
       # print('hhh')
        p = Product.objects.create(name='testp', description='asd')
        self.c = APIClient()

    def test_list(self):
        response = self.c.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            'id': 1, 'name': 'testp', 'description': 'asd', 'price': 0.0, 'scu': '', 
            'gtin': '', 'stock': 0, 'is_available': False, 'image': None}]
        )


    def test_list_paged(self):
        c = APIClient()
        response = self.c.get('/products/?limit=3')
        self.assertEqual(response.status_code, 200)
        # print(response.json())
