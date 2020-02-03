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
            address='first address',
            city='first city', user_profile=self.profile1)
        UserAddress.objects.create(
            address='second address',
            city='second city', user_profile=self.profile1)

    def test_profile_create(self):
        response = self.api_client.post('/users/', {
            'first_name': 'test_isd87yuh',
            'surname': 'testov',
            'patronymic': 'testovich',
            'user': self.test_user4.pk,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        created_profile = UserProfile.objects.get(first_name='test_isd87yuh')
        response_json = response.json()
        uu_id = response_json.pop('uu_id')
        t = uuidTest()
        t.auto_uuid4_test(uu_id)
        self.assertEqual(response_json, {'first_name': 'test_isd87yuh',
                                         'surname': 'testov',
                                         'patronymic': 'testovich',
                                         'user': created_profile.user_id,
                                         'addresses': [],
                                         'phones': []})

    def test_profile_list(self):
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
        pk1 = UserProfile.objects.get(first_name='test1').user_id
        pk2 = UserProfile.objects.get(first_name='test2').user_id
        pk3 = UserProfile.objects.get(first_name='test3').user_id
        expected = [{'addresses': [{'address': 'first address',
                                    'city': 'first city'},
                                   {'address': 'second address',
                                    'city': 'second city'}],
                     'first_name': 'test1',
                     'patronymic': 'testovich1',
                     'phones': [{'phone': '1111'}, {'phone': '2222'}],
                     'surname': 'testov1',
                     'user': pk1},
                    {'addresses': [],
                     'first_name': 'test2',
                     'patronymic': 'testovich2',
                     'phones': [],
                     'surname': 'testov2',
                     'user': pk2},
                    {'addresses': [],
                     'first_name': 'test3',
                     'patronymic': 'testovich3',
                     'phones': [],
                     'surname': 'testov3',
                     'user': pk3}]
        self.assertEqual(response_json, expected)

    def test_profile_list_limit_offset(self):
        response = self.api_client.get('/users/?limit=2&offset=1')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for user_profile in response_json['results']:
            uu_id = user_profile.pop('uu_id')
            t.auto_uuid4_test(uu_id)
        pk2 = UserProfile.objects.get(first_name='test2').user_id
        pk3 = UserProfile.objects.get(first_name='test3').user_id
        expected = {'count': 3,
                    'next': None,
                    'previous': 'http://testserver/users/?limit=2',
                    'results': [{'addresses': [],
                                 'first_name': 'test2',
                                 'patronymic': 'testovich2',
                                 'phones': [],
                                 'surname': 'testov2',
                                 'user': pk2},
                                {'addresses': [],
                                 'first_name': 'test3',
                                 'patronymic': 'testovich3',
                                 'phones': [],
                                 'surname': 'testov3',
                                 'user': pk3}]}
        self.assertEqual(response_json, expected)

    def test_profile_retrieve_positive(self):
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

    def test_profile_retrieve_negative(self):
        request_uuid = uuid.uuid4()
        response = self.api_client.get(f'/users/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 404)

    def test_profile_update(self):
        request_uuid = self.profile2.uu_id
        response = self.api_client.patch(
            f'/users/{str(request_uuid)}/',
            {"first_name": "test2_upd"},
            format='json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.get('uu_id')
        t.auto_uuid4_test(uu_id)
        expected = {'addresses': [],
                    'uu_id': str(self.profile2.uu_id),
                    'first_name': 'test2_upd',
                    'patronymic': 'testovich2',
                    'phones': [],
                    'surname': 'testov2',
                    'user': self.profile2.user_id}
        self.assertEqual(response_json, expected)

    def test_profile_destroy(self):
        request_uuid = self.profile2.uu_id
        response = self.api_client.delete(f'/users/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 204)


class PhoneTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.test_user1 = User.objects.create(
            username='test_user1', password='password')
        self.profile1 = UserProfile.objects.create(
            first_name='test1', surname='testov1',
            patronymic='testovich1', user=self.test_user1)
        self.phone1 = UserPhone.objects.create(
            phone='1111', user_profile=self.profile1)
        self.phone2 = UserPhone.objects.create(
            phone='2222', user_profile=self.profile1)

    def test_phone_create(self):
        user_profile_pk1 = UserProfile.objects.get(first_name='test1').pk
        response = self.api_client.post('/users/phones/', {
            'user_profile': user_profile_pk1,
            'phone': '3333',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        uu_id = response_json.pop('uu_id')
        t = uuidTest()
        t.auto_uuid4_test(uu_id)
        self.assertEqual(response_json, {'phone': '3333',
                                         'user_profile': user_profile_pk1})

    def test_phone_list(self):
        response = self.api_client.get('/users/phones/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for phone in response_json:
            uu_id = phone.pop('uu_id')
            t.auto_uuid4_test(uu_id)
        pk1 = UserPhone.objects.get(phone='1111').user_profile_id
        pk2 = UserPhone.objects.get(phone='2222').user_profile_id
        expected = [{'phone': '1111', 'user_profile': pk1},
                    {'phone': '2222', 'user_profile': pk2}]
        self.assertEqual(response_json, expected)

    def test_phone_list_limit_offset(self):
        response = self.api_client.get('/users/phones/?limit=2&offset=1')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for phone in response_json['results']:
            uu_id = phone.pop('uu_id')
            t.auto_uuid4_test(uu_id)
        pk2 = UserPhone.objects.get(phone='2222').user_profile_id
        expected = {'count': 2,
                    'next': None,
                    'previous': 'http://testserver/users/phones/?limit=2',
                    'results': [{'phone': '2222', 'user_profile': pk2}]}
        self.assertEqual(response_json, expected)

    def test_phone_retrieve_positive(self):
        request_uuid = self.phone2.uu_id
        response = self.api_client.get(f'/users/phones/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.pop('uu_id')
        t.auto_uuid4_test(uu_id)
        pk2 = UserPhone.objects.get(phone='2222').user_profile_id
        expected = {'phone': '2222',
                    'user_profile': pk2}
        self.assertEqual(response_json, expected)

    def test_phone_retrieve_negative(self):
        request_uuid = uuid.uuid4()
        response = self.api_client.get(f'/users/phones/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 404)

    def test_phone_update(self):
        request_uuid = self.phone2.uu_id
        response = self.api_client.patch(
            f'/users/phones/{str(request_uuid)}/',
            {"phone": "2222_upd"},
            format='json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.pop('uu_id')
        t.auto_uuid4_test(uu_id)
        pk2 = UserPhone.objects.get(phone='2222_upd').user_profile_id
        expected = {'phone': '2222_upd', 'user_profile': pk2}
        self.assertEqual(response_json, expected)

    def test_phone_destroy(self):
        request_uuid = self.phone2.uu_id
        response = self.api_client.delete(
            f'/users/phones/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 204)


class AddressTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.test_user1 = User.objects.create(
            username='test_user1', password='password')
        self.profile1 = UserProfile.objects.create(
            first_name='test1', surname='testov1',
            patronymic='testovich1', user=self.test_user1)
        self.address1 = UserAddress.objects.create(
            address='first address',
            city='first city',
            user_profile=self.profile1)
        self.address2 = UserAddress.objects.create(
            address='second address',
            city='second city',
            user_profile=self.profile1)

    def test_address_create(self):
        user_profile_pk1 = UserProfile.objects.get(first_name='test1').pk
        response = self.api_client.post('/users/address/', {
            'user_profile': user_profile_pk1,
            'city': 'third city',
            'address': 'third address'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        uu_id = response_json.pop('uu_id')
        t = uuidTest()
        t.auto_uuid4_test(uu_id)
        self.assertEqual(response_json, {
                         'city': 'third city',
                         'address': 'third address',
                         'user_profile': user_profile_pk1})

    def test_address_list(self):
        response = self.api_client.get('/users/address/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for address in response_json:
            uu_id = address.pop('uu_id')
            t.auto_uuid4_test(uu_id)
        pk1 = UserAddress.objects.get(city='first city').user_profile_id
        pk2 = UserAddress.objects.get(city='second city').user_profile_id
        expected = [{'address': 'first address',
                     'city': 'first city',
                     'user_profile': pk1},
                    {'address': 'second address',
                     'city': 'second city',
                     'user_profile': pk2}]
        self.assertEqual(response_json, expected)

    def test_address_list_limit_offset(self):
        response = self.api_client.get('/users/address/?limit=2&offset=1')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        for address in response_json['results']:
            uu_id = address.pop('uu_id')
            t.auto_uuid4_test(uu_id)
        pk2 = UserAddress.objects.get(city='second city').user_profile_id
        expected = {'count': 2,
                    'next': None,
                    'previous': 'http://testserver/users/address/?limit=2',
                    'results': [{'address': 'second address',
                                 'city': 'second city',
                                 'user_profile': pk2}]}
        self.assertEqual(response_json, expected)

    def test_address_retrieve_positive(self):
        request_uuid = self.address2.uu_id
        response = self.api_client.get(f'/users/address/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.pop('uu_id')
        t.auto_uuid4_test(uu_id)
        pk2 = UserAddress.objects.get(city='second city').user_profile_id
        expected = {'address': 'second address',
                    'city': 'second city',
                    'user_profile': pk2}
        self.assertEqual(response_json, expected)

    def test_address_retrieve_negative(self):
        request_uuid = uuid.uuid4()
        response = self.api_client.get(f'/users/address/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 404)

    def test_address_update(self):
        request_uuid = self.address2.uu_id
        response = self.api_client.patch(
            f'/users/address/{str(request_uuid)}/',
            {"city": "second city upd"},
            format='json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        t = uuidTest()
        uu_id = response_json.pop('uu_id')
        t.auto_uuid4_test(uu_id)
        pk2 = UserAddress.objects.get(city='second city upd').user_profile_id
        expected = {'address': 'second address',
                    'city': 'second city upd',
                    'user_profile': pk2}
        self.assertEqual(response_json, expected)

    def test_address_destroy(self):
        request_uuid = self.address2.uu_id
        response = self.api_client.delete(
            f'/users/address/{str(request_uuid)}/')
        self.assertEqual(response.status_code, 204)
