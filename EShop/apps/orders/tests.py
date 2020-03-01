from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import Order, OrderItem
from apps.products.models import Product


class OrderTest(TestCase):
    
    def setUp(self):
        self.user1=User(username='user1')
        self.user1.set_password("12345")
        self.user1.save()
        self.user2=User(username='user2')
        self.user2.set_password("12345")
        self.user2.save()
        
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
       
        
    def test_order_list(self):
        response = self.c.get('/orders/')
        self.assertEqual(response.status_code, 403)
        self.c.login(username='user1', password='12345')
        response= self.c.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.json()[0]['id'], response.json()[1]['id']), (self.order1.id, self.order3.id)) #orders for user1 - order1, order3
        self.c.logout()
        self.c.login(username='user2', password='12345')
        response = self.c.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.json()[0]['id'], response.json()[1]['id']), (self.order2.id, self.order4.id)) #orders for user2 - order2, order4
        self.c.logout()
        
    def test_order_detail(self):
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
        self.c.logout()
        self.c.login(username='user2', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}')
        self.assertEqual(response.status_code, 404)      #user2 don't have permissions to see order1
        self.c.logout()
        
    def test_orderitem_list(self):
        self.c.login(username='user1', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.json()[0]['id'], response.json()[1]['id']), (self.order1_item1.id, self.order1_item2.id))
        self.c.logout()
        self.c.login(username='user2', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/')
        self.assertEqual(response.status_code, 404)      #user2 don't have permissions
        self.c.logout()
        
    def test_orderitem_detail(self):
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
        self.c.logout()
        self.c.login(username='user2', password='12345')
        response = self.c.get(f'/orders/{self.order1.pub_id}/item/{self.order1_item1.pub_id}/')
        self.assertEqual(response.status_code, 404)       #user2 don't have permissions
        self.c.logout()
       
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
        new_order.delete()
        self.c.logout() 
        
        
    def test_order_delete(self):
        self.c.login(username='user1', password='12345')
        new_order=Order(user=self.user1, accepting_time=timezone.now(), status='completed', is_paid='True')
        new_order.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.status_code, 403)   #cannot delete is_paid and completed order
        new_order.is_paid=False
        new_order.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.status_code, 403)   #cannot delete completed order
        new_order.is_paid=True
        new_order.status='accepted'
        new_order.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.status_code, 403)   #cannot delete is_paid order
        new_order.is_paid=False
        new_order.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.status_code, 204)
        response = self.c.get(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.status_code, 404)
        self.c.logout() 
    
    def test_order_update(self):
        self.c.login(username='user1', password='12345')
        new_order=Order(user=self.user1, accepting_time=timezone.now())
        new_order.save()
        response = self.c.patch(f'/orders/{new_order.pub_id}',{'status':'cancelled'})
        self.assertEqual(response.status_code, 200)
        response = self.c.get(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.json()['status'], 'cancelled')
        response = self.c.patch(f'/orders/{new_order.pub_id}',{'is_paid':True})
        self.assertEqual(response.status_code, 403)     #cannot update cancelled order
        new_order.status='accepted'
        new_order.save()
        response = self.c.patch(f'/orders/{new_order.pub_id}',{'is_paid':True})
        self.assertEqual(response.status_code, 200) 
        response = self.c.get(f'/orders/{new_order.pub_id}')
        self.assertEqual(response.json()['is_paid'], True)
        response = self.c.patch(f'/orders/{new_order.pub_id}',{'status':'cancelled'})
        self.assertEqual(response.status_code, 403)      #cannot update is_paid order
        new_order.delete()
        self.c.logout() 
        
    def test_orderitem_create(self):
        self.c.login(username='user1', password='12345')
        new_order=Order(user=self.user1, accepting_time=timezone.now())
        new_order.save()
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product1.id, 'amount':5}, format='json')
        self.assertEqual(response.status_code, 201)
        new_orderitem=OrderItem.objects.get(order=new_order)
        response = self.c.get(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.status_code, 200)
        json_expected={
                                    'id': new_orderitem.id, 
                                    'pub_id': str(new_orderitem.pub_id), 
                                    'order': new_order.id, 
                                    'product': {'name': 'product1', 'price': 1000.0}, 
                                    'amount': 5
                                    }
        self.assertEqual(response.json(), json_expected)
        new_order.status='completed'
        new_order.save()
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':2}, format='json')
        self.assertEqual(response.status_code, 403)   # cannot add orderitem to completed order
        new_order.is_paid=True
        new_order.status='accepted'
        new_order.save()
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':2}, format='json')
        self.assertEqual(response.status_code, 403)   # cannot add orderitem to is_paid order
        new_order.is_paid=False
        new_order.save()
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':2}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':3}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':4}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':5}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.c.post(f'/orders/{new_order.pub_id}/item/',{'product':self.product2.id, 'amount':6}, format='json')
        self.assertEqual(response.status_code, 403)   # maximum orderitems - 5        
        new_order.delete()
        self.c.logout()
        
    def test_orderitem_delete(self):
        self.c.login(username='user1', password='12345')
        new_order=Order(user=self.user1, accepting_time=timezone.now(), status='completed')
        new_order.save()
        new_orderitem=OrderItem(order=new_order, product=self.product1, amount=10)
        new_orderitem.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.status_code, 403)    #order is completed
        new_order.is_paid=True
        new_order.status='accepted'
        new_order.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.status_code, 403)    #order is_paid
        new_order.is_paid=False
        new_order.save()
        response = self.c.delete(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.status_code, 204)        
        response = self.c.get(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.status_code, 404)
        new_order.delete()
        self.c.logout()
        
    def test_orderitem_update(self):
        self.c.login(username='user1', password='12345')
        new_order=Order(user=self.user1, accepting_time=timezone.now(), status='completed')
        new_order.save()
        new_orderitem=OrderItem(order=new_order, product=self.product1, amount=10)
        new_orderitem.save()
        response = self.c.patch(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/',{'amount':20})
        self.assertEqual(response.status_code, 403)    #order is completed
        new_order.is_paid=True
        new_order.status='accepted'
        new_order.save()
        response = self.c.patch(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/',{'amount':20})
        self.assertEqual(response.status_code, 403)    #order is_paid
        new_order.is_paid=False
        new_order.save()
        response = self.c.patch(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/',{'amount':20})
        self.assertEqual(response.status_code, 200)        
        response = self.c.get(f'/orders/{new_order.pub_id}/item/{new_orderitem.pub_id}/')
        self.assertEqual(response.json()['amount'], 20)
        new_order.delete()
        self.c.logout()

        
            
        
        
