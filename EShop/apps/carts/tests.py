from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.carts.models import Cart, CartItem
from apps.products.models import Product
from django.contrib.auth.models import User


class CartsAndCartItemsTestAPI(TestCase):

    def setUp(self):
        product_1 = Product.objects.create(name = 'test_pr', description = 'descrip_of_pr')
        user_1 = User.objects.create_user(username = 'Li')
        cart_1 = Cart.objects.create(user = user_1)
        cart_item_1 = CartItem.objects.create(cart = cart_1, product = product_1)

        cart_2 = Cart.objects.create(user = user_1)
        cart_3 = Cart.objects.create(user = user_1)
        cart_item_2 = CartItem.objects.create(cart = cart_2, product = product_1)

        self.c = APIClient()


    def test_cart_item_list(self):
        response = self.c.get('/carts/item/')
        self.assertEqual(response.status_code, 200)
        print(response.status_code)
#        print(response.json(), len(response.json()))

    def test_cart_item_list_paged(self):
        response = self.c.get('/carts/item/?limit=5')
        self.assertEqual(response.status_code, 200)
        print(response.status_code)        
#        print(response.json())

    def test_cart_item_list_amount(self):
        response = self.c.get('/carts/item/')
        self.assertEqual(len(response.json()), 2)
        print(len(response.json()))

    def test_cart_list(self):
        response = self.c.get('/carts/')
        self.assertEqual(response.status_code, 200)
        print(response.status_code)
#        print(response.json())

    def test_cart_list_paged(self):
        response = self.c.get('/carts/?limit=3')
        self.assertEqual(response.status_code, 200)
        print(response.status_code)        
#        print(response.json())
        
    def test_cart_list_amount(self):
        response = self.c.get('/carts/')
        self.assertEqual(len(response.json()), 3)
        print(len(response.json()))
     


 
 

 

