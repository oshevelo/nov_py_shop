from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import Order


class OrderTest(TestCase):
    
    def setUp(self):
        self.user1=User(username='aaa')
        self.user1.set_password("12345")
        self.user1.save()
        self.user2=User(username='bbb')
        self.user2.set_password("12345")
        self.user2.save()
        self.order1=Order(user=self.user1, accepting_time=timezone.now())
        self.order2=Order(user=self.user2, accepting_time=timezone.now()-datetime.timedelta(hours=2), 
                                        completing_or_rejecting_time=timezone.now()+datetime.timedelta(hours=1),
                                        status='completed')
        self.order1.save()
        self.order2.save()
        self.c = APIClient()
        
    def test_order_list(self):
        response = self.c.get('/orders/')
        self.assertEqual(response.status_code, 403)
        self.c.login(username='aaa', password='12345')
        response_user1 = self.c.get('/orders/')
        self.assertEqual(response_user1.status_code, 200)
        self.c.logout()
        self.c.login(username='bbb', password='12345')
        response_user2 = self.c.get('/orders/')
        self.assertEqual(response_user2.status_code, 200)
        self.c.logout()
        self.assertNotEqual(response_user1.json(), response_user2.json())
        
    def test_order_detail(self):
        order1_pub_id=self.order1.pub_id
        order2_pub_id=self.order2.pub_id
        self.c.login(username='aaa', password='12345')
        response = self.c.get(f'/orders/{order2_pub_id}')
        self.assertEqual(response.status_code, 404)
        response = self.c.get(f'/orders/{order1_pub_id}')
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        self.c.logout()
        
       
