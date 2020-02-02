from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import UserProfile, UserPhone, UserAddress
from django.contrib.auth.models import User
import uuid
from pprint import pprint


class uuidTest(TestCase):

    def auto_uuid4_test(self, uu_id):
        obj = uuid.UUID(uu_id)
        self.assertTrue(obj)
        self.assertEquals(len(obj.hex), 32)
        self.assertTrue(isinstance(obj, uuid.UUID))
        self.assertEquals(obj.version, 4)


class ProfileTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.test_user1 = User.objects.create(
            username='test_user1', password='password')
        self.test_user2 = User.objects.create(
            username='test_user2', password='password')
        self.test_user3 = User.objects.create(
            username='test_user3', password='password')
        self.test_user4 = User.objects.create(
            username='test_user4', password='password')
        self.profile1 = UserProfile.objects.create(
            first_name='test1', surname='testov1',
            patronymic='testovich1', user=self.test_user1)
        self.profile2 = UserProfile.objects.create(
            first_name='test2', surname='testov2',
            patronymic='testovich2', user=self.test_user2)
        self.profile3 = UserProfile.objects.create(
            first_name='test3', surname='testov3',
            patronymic='testovich3', user=self.test_user3)
        UserPhone.objects.create(phone='1111', user_profile=self.profile1)
        UserPhone.objects.create(phone='2222', user_profile=self.profile1)
        UserAddress.objects.create(
            address='first address', city='first city', user_profile=self.profile1)
        UserAddress.objects.create(
            address='second address', city='second city', user_profile=self.profile1)

    def test_01_profile_create(self):
        response = self.api_client.post('/users/', {
            'first_name': 'test123321!!',
            'surname': 'testov',
            'patronymic': 'testovich',
            'user': self.test_user4.pk,
        }, format='json')
        #created_profile = UserProfile.objects.get(first_name='test123321!!')
        #created_profile.pk
        
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        uu_id = response_json.pop('uu_id')
        t = uuidTest()
        t.auto_uuid4_test(uu_id)
        '''
        self.assertEqual(response_json, {'first_name': 'test123321!!',
                                         'surname': 'testov',
                                         'created_at': created_profile.created_at,
                                         'created_at': response_json['created_at'],
                                         'user': 4, 'addresses': [],
                                         'phones': []})
        '''
        self.assertEqual(response_json, {'first_name': 'test123321!!',
                                         'surname': 'testov',
                                         'patronymic': 'testovich',
                                         'user': 4, 'addresses': [],
                                         'phones': []})

    def test_02_profile_list(self):
        response = self.api_client.get('/users/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for user_profile in response_json:
            uu_id = user_profile.pop('uu_id')
            t.auto_uuid4_test(uu_id)
            for address in user_profile['addresses']:
                uu_id = address.pop('uu_id')
                t.auto_uuid4_test(uu_id)
            for phone in user_profile['phones']:
                uu_id = phone.pop('uu_id')
                t.auto_uuid4_test(uu_id)
        expected = [{'addresses': [{'address': 'first address', 'city': 'first city'},
                                   {'address': 'second address', 'city': 'second city'}],
                     'first_name': 'test1',
                     'patronymic': 'testovich1',
                     'phones': [{'phone': '1111'}, {'phone': '2222'}],
                     'surname': 'testov1',
                     'user': 5},
                    {'addresses': [],
                     'first_name': 'test2',
                     'patronymic': 'testovich2',
                     'phones': [],
                     'surname': 'testov2',
                     'user': 6},
                    {'addresses': [],
                     'first_name': 'test3',
                     'patronymic': 'testovich3',
                     'phones': [],
                     'surname': 'testov3',
                     'user': 7}]
        self.assertEqual(response_json, expected)

    def test_03_profile_list_limit_offset(self):
        response = self.api_client.get('/users/?limit=2&offset=1')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for user_profile in response_json['results']:
            uu_id = user_profile.pop('uu_id')
            t.auto_uuid4_test(uu_id)
        expected = {'count': 3,
                    'next': None,
                    'previous': 'http://testserver/users/?limit=2',
                    'results': [{'addresses': [],
                                 'first_name': 'test2',
                                 'patronymic': 'testovich2',
                                 'phones': [],
                                 'surname': 'testov2',
                                 'user': 10},
                                {'addresses': [],
                                 'first_name': 'test3',
                                 'patronymic': 'testovich3',
                                 'phones': [],
                                 'surname': 'testov3',
                                 'user': 11}]}
        self.assertEqual(response_json, expected)

    def test_04_profile_retrieve_positive(self):
        request_uuid = self.profile2.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.pop('uu_id')
        t.auto_uuid4_test(uu_id)
        expected = {'first_name': 'test2',
                    'surname': 'testov2',
                    'patronymic': 'testovich2',
                    'user': self.profile2.user_id,
                    'addresses': [],
                    'phones': []}
        self.assertEqual(response_json, expected)

    def test_05_profile_retrieve_negative(self):
        request_uuid = uuid.uuid4()
        response = self.api_client.get(f'/users/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 404)

    def test_06_profile_update(self):
        request_uuid = self.profile2.uu_id
        response = self.api_client.patch(
            f'/users/{str(request_uuid)}/', {"first_name": "test2_upd"}, format='json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.get('uu_id')
        t.auto_uuid4_test(uu_id)
        expected = {'addresses': [],
                    'uu_id': self.profile2.uu_id,
                    'first_name': 'test2_upd',
                    'patronymic': 'testovich2',
                    'phones': [],
                    'surname': 'testov2',
                    'user': self.profile2.user_id}
        self.assertEqual(response_json, expected)

    def test_07_profile_destroy(self):
        request_uuid = self.profile2.uu_id
        response = self.api_client.delete(f'/users/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 204)


