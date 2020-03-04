from django.test import TestCase
from rest_framework.test import APIClient
from apps.carts.models import Cart, CartItem
from apps.products.models import Product
from django.contrib.auth.models import User
from datetime import datetime 
import uuid



class CartsAndCartItemsTestAPI(TestCase):


    def setUp(self):
        
        self.user_1 = User(username='Li_1')
        self.user_1.set_password('password_1')
        self.user_1.save()

#        self.user_2 = User(username='Li_2')
#        self.user_2.set_password('password_2')
#        self.user_2.save()

#        self.user_1 = User.objects.create_user(username='Li_1', password='password_1')
        self.user_2 = User.objects.create_user(username='Li_2', password='password_2')
     
        product_1 = Product.objects.create(name='test_pr_1', description='descrip_of_pr_1')
        product_2 = Product.objects.create(name='test_pr_2', description='descrip_of_pr_2')
        product_3 = Product.objects.create(name='test_pr_3', description='descrip_of_pr_3')        
        
        self.cart_1 = Cart.objects.create(user=self.user_1)
        self.cart_2 = Cart.objects.create(user=self.user_1)
        self.cart_3 = Cart.objects.create(user=self.user_2)
       
        self.cart_item_1 = CartItem.objects.create(cart=self.cart_1, product=product_1)               
        self.cart_item_2 = CartItem.objects.create(cart=self.cart_2, product=product_2)
        self.cart_item_3 = CartItem.objects.create(cart=self.cart_3, product=product_3)

        self.c = APIClient()



    def test_cart_list(self):
        response = self.c.get('/carts/') 
        self.assertEqual(response.status_code, 403) 
           
        self.c.login(username='Li_1', password='password_1')
        response_user_1 = self.c.get('/carts/')
        self.assertEqual(response_user_1.status_code, 200)
        self.c.logout()

        self.c.login(username='Li_2', password='password_2')
        response_user_2 = self.c.get('/carts/')
        self.assertEqual(response_user_2.status_code, 200)
        self.c.logout()


    def test_cart_list_negative(self):        
        self.c.login(username='Li_1', password='password_2')   # incorrect password
        response_user_1 = self.c.get('/carts/')
        self.assertEqual(response_user_1.status_code, 403)
        
 
    def test_cart_retrieve(self):
        cart_uuid = self.cart_3.public_id
        self.c.login(username='Li_2', password='password_2')
        response = self.c.get(f'/carts/{cart_uuid}/')
        self.assertEqual(response.status_code, 200)
        self.c.logout()


    def test_cart_retrieve_negative(self):
        cart_uuid = self.cart_item_3.public_id    # incorrect cart.public_id  
        self.c.login(username='Li_2', password='password_2')
        response = self.c.get(f'/carts/{cart_uuid}/')
        self.assertEqual(response.status_code, 404)
        self.c.logout()
     

    def test_cart_create(self):
        self.c.login(username='Li_1', password='password_1')
        response = self.c.post('/carts/', {'user': self.user_1.pk, 'items': [{'product': {'name': 'test_pr_2', 'price': 0.0}}]}, format='json')
#        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(isinstance(uuid.UUID(response.json()['public_id']), uuid.UUID))
        self.c.logout()


    def test_cart_update(self):
        cart_uuid = self.cart_3.public_id
        self.c.login(username='Li_2', password='password_2')
#        new_datetime = datetime.utcnow().isoformat() + 'Z'
        new_datetime = datetime.utcnow().strftime('% Y-% m-% dT% H:% M:% S.% fZ')
        response = self.c.patch(f'/carts/{cart_uuid}/', {'updated_at': new_datetime})
        self.assertEqual(response.status_code, 200)
        self.c.logout()


    def test_cart_destroy(self):
        cart_uuid = self.cart_2.public_id
        self.c.login(username='Li_1', password='password_1')
        response = self.c.delete(f'/carts/{cart_uuid}/')
        self.assertEqual(response.status_code, 204)
        updated_response = self.c.delete(f'/carts/{cart_uuid}/')
        self.assertEqual(updated_response.status_code, 404)        

# 'items': [{'id': 5, 'public_id': 'b5e7e7d8-31c6-44ef-abe2-bc5210505c6a', 'product': {'name': 'test_pr_2', 'price': 0.0}, 'quantity': 1, 'created_at': '2020-02-26T19:30:53.932136Z', 'updated_at': '2020-02-26T19:30:53.932149Z'}]    


    def test_cart_item_list(self):
        cart_uuid = self.cart_3.public_id
#        print(cart_uuid)
        self.c.login(username='Li_2', password='password_2')
        response = self.c.get(f'/carts/{cart_uuid}/item/')
#        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 200) 
        self.c.logout()


    def test_cart_item_list_create(self):
        cart_uuid = self.cart_1.public_id
        self.c.login(username='Li_1', password='password_1')
        response = self.c.post(f'/carts/{cart_uuid}/item/', {'cart': self.cart_1.pk, 'product': {'name': 'test_pr_2', 'price': 0.0}}, format='json')
        print(response.json(), response.status_code)
        self.assertEqual(response.status_code, 201)
        self.c.logout()


    def test_cart_item_retrieve(self):
        cart_uuid = self.cart_3.public_id
        cart_item_uuid = self.cart_item_3.public_id
        self.c.login(username='Li_2', password='password_2')
        response = self.c.get(f'/carts/{cart_uuid}/item/{cart_item_uuid}/')
#        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        self.c.logout()


    def test_cart_item_retrieve_negative(self):
        cart_uuid = self.cart_2.public_id
        cart_item_uuid = self.cart_2.public_id    # incorrect cart_item.public_id 
        self.c.login(username='Li_1', password='password_1')
        response = self.c.get(f'/carts/{cart_uuid}/item/{cart_item_uuid}/')
        self.assertEqual(response.status_code, 404)
        self.c.logout()


    def test_cart_item_update(self):
        cart_uuid = self.cart_2.public_id
        cart_item_uuid = self.cart_item_2.public_id
        self.c.login(username='Li_1', password='password_1')
#        new_datetime = datetime.utcnow().isoformat() + 'Z'
        new_datetime = datetime.utcnow().strftime('% Y-% m-% dT% H:% M:% S.% fZ')
        response = self.c.patch(f'/carts/{cart_uuid}/item/{cart_item_uuid}/', {'updated_at': new_datetime})
        self.assertEqual(response.status_code, 200)
        self.c.logout()

  
    def test_cart_item_destroy(self):
        cart_uuid = self.cart_2.public_id
        cart_item_uuid = self.cart_item_2.public_id
        self.c.login(username='Li_1', password='password_1')
        response = self.c.delete(f'/carts/{cart_uuid}/item/{cart_item_uuid}/')
        self.assertEqual(response.status_code, 204)
        updated_response = self.c.delete(f'/carts/item/{cart_item_uuid}/')
        self.assertEqual(updated_response.status_code, 404)       



    
#    !!! Previous_Tests !!!
#    Cart_Tests

"""
    
    def test_cart_create(self):
        response = self.c.post('/carts/', {'user': self.user_1.pk}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(isinstance(uuid.UUID(response.json()['public_id']), uuid.UUID))

    def test_cart_list(self):
        response = self.c.get('/carts/')
        self.assertEqual(response.status_code, 200)

    def test_cart_list_amount(self):
        response = self.c.get('/carts/')
        self.assertEqual(len(response.json()), 3)

    def test_cart_list_paged(self):
        response = self.c.get('/carts/?limit=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)

    def test_cart_list_limit_offset(self):
        response = self.c.get('/carts/?limit=2&offset=1')
        self.assertEqual(response.status_code, 200) 
        result_1_on_current_page = response.json()['results'][0]     # check : cart_2 ==> user_1 
#        print(result_1_on_current_page['user'])
        self.assertEqual(result_1_on_current_page['user'], self.user_1.pk)

    def test_cart_retrieve(self):
        cart_uuid = self.cart_3.public_id
        response = self.c.get(f'/carts/{cart_uuid}/')
        self.assertEqual(response.status_code, 200)

    def test_cart_retrieve_negative(self):
        cart_uuid = self.cart_item_3.public_id    # incorrect cart.public_id  
        response = self.c.get(f'/carts/{cart_uuid}/')
        self.assertEqual(response.status_code, 404)

    def test_cart_update(self):
        cart_uuid = self.cart_3.public_id
#        new_datetime = datetime.utcnow().isoformat() + 'Z'
        new_datetime = datetime.utcnow().strftime('% Y-% m-% dT% H:% M:% S.% fZ')
        response = self.c.patch(f'/carts/{cart_uuid}/', {'updated_at': new_datetime})
        self.assertEqual(response.status_code, 200)

    def test_cart_destroy(self):
        cart_uuid = self.cart_2.public_id
        response = self.c.delete(f'/carts/{cart_uuid}/')
        self.assertEqual(response.status_code, 204)
        updated_response = self.c.delete(f'/carts/{cart_uuid}/')
        self.assertEqual(updated_response.status_code, 404)        
"""  
 
#    CartItem_Tests

"""
    def test_cart_item_create(self):       
        response = self.c.post('/carts/item/', {'cart': self.cart_2.pk }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(isinstance(uuid.UUID(response.json()['public_id']), uuid.UUID))

    def test_cart_item_list(self):
        response = self.c.get('/carts/item/')
        self.assertEqual(response.status_code, 200)

    def test_cart_item_list_amount(self):
        response = self.c.get('/carts/item/')
        self.assertEqual(len(response.json()), 3)

    def test_cart_item_list_paged(self):
        response = self.c.get('/carts/item/?limit=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)

    def test_cart_item_list_limit_offset(self):
        response = self.c.get('/carts/item/?limit=2&offset=0')
        self.assertEqual(response.status_code, 200)
        result_2_on_current_page = response.json()['results'][1]    # check : cart_item_2 ==> cart_2
        self.assertEqual(result_2_on_current_page['cart'], self.cart_2.pk)

    def test_cart_item_retrieve(self):
        cart_item_uuid = self.cart_item_2.public_id
        response = self.c.get(f'/carts/item/{cart_item_uuid}/')
        self.assertEqual(response.status_code, 200)

    def test_cart_item_retrieve_negative(self):
        cart_item_uuid = self.cart_2.public_id    # incorrect cart_item.public_id 
        response = self.c.get(f'/carts/item/{cart_item_uuid}/')
        self.assertEqual(response.status_code, 404)

    def test_cart_item_update(self):
        cart_item_uuid = self.cart_item_2.public_id
#        new_datetime = datetime.utcnow().isoformat() + 'Z'
        new_datetime = datetime.utcnow().strftime('% Y-% m-% dT% H:% M:% S.% fZ')
        response = self.c.patch(f'/carts/item/{cart_item_uuid}/', {'updated_at': new_datetime})
        self.assertEqual(response.status_code, 200)
  
    def test_cart_item_destroy(self):
        cart_item_uuid = self.cart_item_2.public_id
        response = self.c.delete(f'/carts/item/{cart_item_uuid}/')
        self.assertEqual(response.status_code, 204)
        updated_response = self.c.delete(f'/carts/item/{cart_item_uuid}/')
        self.assertEqual(updated_response.status_code, 404)        
"""

 

