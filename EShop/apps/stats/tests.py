from django.test import TestCase
from rest_framework.test import APIClient
from apps.stats.models import Stat
from apps.users.models import UserProfile, UserPhone, UserAddress
from django.contrib.auth.models import User
import uuid
from pprint import pprint
from datetime import datetime


class TimeTest(TestCase):

    def check_time(self, time_str):
        obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEquals(type(obj), datetime)


class ProfileTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin', password='admin_password', email='email')
        self.test_user1 = User.objects.create_user(
            username='test_user1', password='password1')
        self.test_user2 = User.objects.create_user(
            username='test_user2', password='password2')

    def test_stat_create_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        response = self.api_client.post(f'/stats/add/', {
            'action': 'browse_product',
            'additional_info': {'product_id': 1}
        }, format='json')
        self.assertEqual(response.status_code, 201)
        response_obj = response.json()
        t = TimeTest()
        t.check_time(response_obj.pop('created'))
        expected = {'action': 'browse_product',
                    'additional_info': {'product_id': 1}}
        self.assertEqual(response_obj, expected)

    def test_stat_create_negative(self):
        response = self.api_client.post(f'/stats/add/', {
            'action': 'browse_product',
            'additional_info': {'product_id': 1}
        }, format='json')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)
