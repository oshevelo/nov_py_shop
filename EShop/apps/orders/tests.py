from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import Order, OrderItem
from apps.products.models import Product
from apps.shipments.models import Shipment


class OrderTest(TestCase):
    
    def setUp(self):
        self.user1=User.objects.create_user(username='user1', password='12345')
        self.user2=User.objects.create_user(username='user2', password='12345')
        
        self.product1=Product(name='product1', price=1000, scu='111', gtin='11111', is_available=True)
        self.product1.save()
        self.product2=Product(name='product2', price=2000, scu='222', gtin='22222', is_available=True)
        self.product2.save()
        
        self.order1=Order(user=self.user1, accepting_time=timezone.now()-datetime.timedelta(hours=1))
        self.order1.save()
        self.order2=Order(user=self.user2, accepting_time=timezone.now()-datetime.timedelta(hours=2))
        self.order2.save()
        self.order3=Order(user=self.user1, accepting_time=timezone.now()-datetime.timedelta(hours=3))
        self.order3.save()
        self.order4=Order(user=self.user2, accepting_time=timezone.now()-datetime.timedelta(hours=4))
        self.order4.save()
                                        
        self.order1_item1=OrderItem(order=self.order1, product=self.product1, amount=1)
        self.order1_item1.save()
        self.order1_item2=OrderItem(order=self.order1, product=self.product2, amount=2)
        self.order1_item2.save()

        self.c = APIClient()
       
        
    def test_order_list_unauthorized(self):
        response = self.c.get('/orders/')
        self.assertEqual(response.status_code, 403)
    
    def test_order_list_user1(self):
        self.c.login(username='user1', password='12345')
        response= self.c.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.json()[0]['id'], response.json()[1]['id']), (self.order1.id, self.order3.id)) #orders for user1 - order1, order3
        
    def test_order_list_user2(self):
        self.c.login(username='user2', password='12345')
        response = self.c.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.json()[0]['id'], response.json()[1]['id']), (self.order2.id, self.order4.id)) #orders for user2 - order2, order4
        
    def test_order_detail_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 200)
        json_expected={
                                    'id': self.order1.id, 
                                    'pub_id': str(self.order1.pub_id), 
                                    'user': self.user1.id, 
                                    'accepting_time': self.order1.accepting_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 
                                    'completing_or_rejecting_time': None, 
                                    'status': 'accepted', 
                                    'is_paid': False, 
                                    'is_editable': True, 
                                    'max_orderitems': False, 
                                    'comment': '', 
                                    'orderitems': [
                                    {
                                    'id': self.order1_item1.id, 
                                    'pub_id': str(self.order1_item1.pub_id), 
                                    'order': self.order1.id, 
                                    'product': self.product1.id, 
                                    'amount': 1
                                    }, 
                                    {
                                    'id': self.order1_item2.id, 
                                    'pub_id': str(self.order1_item2.pub_id), 
                                    'order': self.order1.id, 
                                    'product': self.product2.id, 
                                    'amount': 2
                                    }
                                    ]
                                    }
        self.assertEqual(response.json(), json_expected)
        
    def test_order_detail_fail(self):
        self.c.login(username='user2', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 404)      #user2 don't have permissions to see order1
        
    def test_orderitem_list_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.json()[0]['id'], response.json()[1]['id']), (self.order1_item1.id, self.order1_item2.id))
        
    def test_orderitem_list_fail(self):
        self.c.login(username='user2', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/')
        self.assertEqual(response.status_code, 404)      #user2 don't have permissions
        
    def test_orderitem_detail_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 200)
        json_expected={
                                    'id': self.order1_item1.id, 
                                    'pub_id': str(self.order1_item1.pub_id), 
                                    'order': self.order1.id, 
                                    'product': {'name': 'product1', 'price': 1000.0}, 
                                    'amount': 1
                                    }
        self.assertEqual(response.json(), json_expected)
        
    def test_orderitem_detail_fail(self):
        self.c.login(username='user2', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 404)       #user2 don't have permissions
       
    def test_order_create(self):
        self.c.login(username='user1', password='12345')
        response= self.c.post('/orders/', {'accepting_time':str(datetime.datetime.now()), 'status':'completed', 'is_paid':True, 'comment':'test_order_create'}, format='json')
        self.assertEqual(response.status_code, 201)
        new_order=Order.objects.get(comment='test_order_create')
        response = self.c.get(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.status_code, 200)
        json_expected={
                                    'id': new_order.id, 
                                    'pub_id': str(new_order.pub_id), 
                                    'user': self.user1.id, 
                                    'accepting_time': new_order.accepting_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 
                                    'completing_or_rejecting_time': None, 
                                    'status': 'completed', 
                                    'is_paid': True, 
                                    'is_editable': False, 
                                    'max_orderitems': False, 
                                    'comment': 'test_order_create', 
                                    'orderitems': []
                                    }
        self.assertEqual(response.json(), json_expected)
                
    def test_order_delete_is_paid_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.is_paid=True
        self.order1.save()
        response = self.c.delete(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 403)   #cannot delete is_paid order
        
    def test_order_delete_completed_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.status='completed'
        self.order1.save()
        response = self.c.delete(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 403)   #cannot delete completed order
        
    def test_order_delete_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.delete(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 204)
        response = self.c.get(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 404)
    
    def test_order_update_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.patch(f'/orders/{self.order1.pub_id}',{'status':'cancelled'})
        self.assertEqual(response.status_code, 200)
        response = self.c.get(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.json()['status'], 'cancelled')
        
    def test_order_update_is_paid_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.is_paid=True
        self.order1.save()
        response = self.c.patch(f'/orders/{self.order1.pub_id}',{'status':'cancelled'})
        self.assertEqual(response.status_code, 403)      #cannot update is_paid order
        
    def test_order_update_completed_fail(self):
        self.order1.status='completed'
        self.order1.save()
        response = self.c.patch(f'/orders/{self.order1.pub_id}',{'status':'cancelled'})
        self.assertEqual(response.status_code, 403)     #cannot update completed order                
        
    def test_orderitem_create_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product1.id, 'amount':5}, format='json')
        self.assertEqual(response.status_code, 201)
        new_orderitem=OrderItem.objects.get(amount=5)
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.status_code, 200)
        json_expected={
                                    'id': new_orderitem.id, 
                                    'pub_id': str(new_orderitem.pub_id), 
                                    'order': self.order1.id, 
                                    'product': {'name': 'product1', 'price': 1000.0}, 
                                    'amount': 5
                                    }
        self.assertEqual(response.json(), json_expected)
        
    def test_orderitem_create_completed_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.status='completed'
        self.order1.save()
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product1.id, 'amount':5}, format='json')
        self.assertEqual(response.status_code, 403)   # cannot add orderitem to completed order
        
    def test_orderitem_create_is_paid_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.is_paid=True
        self.order1.save()
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product1.id, 'amount':5}, format='json')
        self.assertEqual(response.status_code, 403)   # cannot add orderitem to is_paid order
        
    def test_orderitem_create_maximum(self):
        self.c.login(username='user1', password='12345')
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product2.id, 'amount':3}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product2.id, 'amount':4}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product2.id, 'amount':5}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{self.order1.pub_id}/item/',{'product':self.product2.id, 'amount':6}, format='json')
        self.assertEqual(response.status_code, 403)   # maximum orderitems - 5         
        
    def test_orderitem_delete_completed_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.status='completed'
        self.order1.save()
        response = self.c.delete(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 403)    #order is completed
        
    def test_orderitem_delete_is_paid_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.is_paid=True
        self.order1.save()
        response = self.c.delete(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 403)    #order is_paid
        
    def test_orderitem_delete_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.delete(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 204)
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 404)
                      
    def test_orderitem_update_completed_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.status='completed'
        self.order1.save()
        response = self.c.patch(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/',{'amount':10})
        self.assertEqual(response.status_code, 403)    #order is completed
        
    def test_orderitem_update_is_paid_fail(self):
        self.c.login(username='user1', password='12345')
        self.order1.is_paid=True
        self.order1.save()
        response = self.c.patch(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/',{'amount':10})
        self.assertEqual(response.status_code, 403)    #order is_paid
        
    def test_orderitem_update_success(self):
        self.c.login(username='user1', password='12345')
        response = self.c.patch(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/',{'amount':10})
        self.assertEqual(response.status_code, 200)
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.json()['amount'], 10)
        
    def test_create_shipment(self):
        self.c.login(username='user1', password='12345')
        post_json={
                            'shipment_type':'HOME',  
                            'destination_city':'Kyiv',
                            'destination_zip_code':'111',
                            'destination_adress_street':'Peremohy',
                            'destination_adress_building':'1a'
                            }
        response = self.c.post(f'/orders/{self.order1.pub_id}/create_shipment', post_json,  format='json')
        self.assertEqual(response.status_code, 201)
        new_shipment=Shipment.objects.get(destination_city='Kyiv')
        json_expected={
                                    'id': new_shipment.id, 
                                    'uuid': str(new_shipment.uuid), 
                                    'shipment_type': 'HOME', 
                                    'shipment_date': None, 
                                    'destination_city': 'Kyiv', 
                                    'destination_zip_code': 111, 
                                    'destination_adress_street': 'Peremohy', 
                                    'destination_adress_building': '1a', 
                                    'destination_other_details': ''
                                    }
        self.assertEqual(response.json(), json_expected) 
        response = self.c.post(f'/orders/{self.order1.pub_id}/create_shipment', post_json,  format='json')
        self.assertEqual(response.status_code, 403)   # shipment for order is already exists