from django.test import TestCase
from rest_framework.test import APIClient
from apps.shipments.models import Shipment
from apps.orders.models import Order
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

class shipmentsTest(TestCase):

    def setUp(self):
        self.sh=APIClient()
        self.user_1=User.objects.create(username="Test", password="Test")
        self.order_1 = Order.objects.create(user=self.user_1, accepting_time=now())
        self.shipment_1=Shipment.objects.create(order=self.order_1,destination_city="Testville", destination_zip_code = 1111, destination_adress_street="Test str", destination_adress_building="1a")
        print(self.shipment_1.uuid)

    def test_shipment_create(self):   
        response=self.sh.post('/shipments/', 
        {'order': self.order_1.id,
         'destination_city': 'test',
         'destination_zip_code': '11111',
         'destination_adress_street': 'test',
         'destination_adress_building': '1t',
        }, format='json')
        print(response.json())
        self.assertEqual(response.status_code, 201)

    def test_shipment_list(self):
        response = self.sh.get('/shipments/')
        self.assertEqual(response.status_code, 200)

    def test_shipment_retrieve(self):
        uuid = self.shipment_1.uuid
        response = self.sh.get('/shipments/{}'.format(uuid))
        self.assertEqual(response.status_code, 200)

    def test_shipment_retrieve_negative(self):
        uuid = "1234"  #invalid uuid
        response = self.sh.get('/shipments/{}'.format(uuid))
        self.assertEqual(response.status_code, 404)

    def test_shipment_list_paged(self):
        response = self.sh.get('/shipments/?limit=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
    
    def test_shipment_destroy(self):
        uuid = self.shipment_1.uuid
        response = self.sh.delete('/shipments/{}'.format(uuid))
        self.assertEqual(response.status_code, 204)
        updated_response = self.sh.delete('/shipments/{}'.format(uuid))
        self.assertEqual(updated_response.status_code, 404)
 

    def test_shipment_update(self):
        uuid = self.shipment_1.uuid
        new_destination_city = "Testopolis"
        response = self.sh.patch('/shipments/{}'.format(uuid), 
                                 {'destination_city': new_destination_city})
        self.assertEqual(response.status_code, 200)


"""

    def test_shipment_update(self):
        uuid = self.shipment_1.uuid
        new_destination_city = "Testopolis"
        response = self.sh.patch(f'/shipments/{uuid}/', {'destination_city': new_destination_city})
        self.assertEqual(response.status_code, 200)
 
"""

    
        
            
