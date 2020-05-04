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

    def process_object_uuids(self, obj):
        res_obj = type(obj)()
        if type(obj) is list:
            for elem in obj:
                res_obj.append(self.process_object_uuids(elem))
        else:
            for item in obj:
                if item == 'uu_id':
                    uu_id = obj[item]
                    self.auto_uuid4_test(uu_id)
                elif type(obj[item]) is list:
                    res_obj[item] = self.process_object_uuids(obj[item])
                else:
                    res_obj[item] = obj[item]
        return res_obj


class ProfileTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin', password='admin_password', email='email')
        self.test_user1 = User.objects.create_user(
            username='test_user1', password='password1')
        self.test_user2 = User.objects.create_user(
            username='test_user2', password='password2')

        self.profile1 = UserProfile.objects.get(
            user=self.test_user1)
        self.profile1.first_name = 'test1'
        self.profile1.surname = 'testov1'
        self.profile1.patronymic = 'testovich1'
        self.profile1.save()
        self.profile2 = UserProfile.objects.get(
            user=self.test_user2)
        self.profile2.first_name = 'test2'
        self.profile2.surname = 'testov2'
        self.profile2.patronymic = 'testovich2'
        self.profile2.save()

        self.phone1 = UserPhone.objects.create(
            phone='1111', user_profile=self.profile1)
        self.phone2 = UserPhone.objects.create(
            phone='2222', user_profile=self.profile1)
        self.phone3 = UserPhone.objects.create(
            phone='3333', user_profile=self.profile2)
        self.phone4 = UserPhone.objects.create(
            phone='4444', user_profile=self.profile2)

        self.address1 = UserAddress.objects.create(
            address='first address',
            city='first city', user_profile=self.profile1)
        self.address2 = UserAddress.objects.create(
            address='second address',
            city='second city', user_profile=self.profile1)
        self.address3 = UserAddress.objects.create(
            address='third address',
            city='third city', user_profile=self.profile2)

    def test_profile_create(self):
        new_user = User.objects.create_user(
            username='new_user',
            password='new_password'
        )
        new_user_profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(
            type(new_user_profile),
            type(UserProfile.objects.all()[0])
        )

    def test_profile_list_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        response = self.api_client.get('/users/')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = [{'addresses':
                     [{'address': 'first address',
                       'city': 'first city'},
                         {'address': 'second address',
                          'city': 'second city'}],
                     'avatar': None,
                     'cart': None,
                     'first_name': 'test1',
                     'last_seen_products': [],
                     'orders': [],
                     'patronymic': 'testovich1',
                     'phones': [{'phone': '1111'},
                                {'phone': '2222'}],
                     'surname': 'testov1'}]
        self.assertEqual(processed_response, expected)

    def test_profile_list_negative(self):
        response = self.api_client.get('/users/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

    def test_profile_retrieve_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid1)}/')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'addresses':
                    [{'address': 'first address',
                      'city': 'first city'},
                     {'address': 'second address',
                      'city': 'second city'}],
                    'avatar': None,
                    'cart': None,
                    'first_name': 'test1',
                    'last_seen_products': [],
                    'orders': [],
                    'patronymic': 'testovich1',
                    'phones': [{'phone': '1111'},
                               {'phone': '2222'}],
                    'surname': 'testov1'}
        self.assertEqual(processed_response, expected)

    def test_profile_retrieve_negative(self):
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid1)}/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.get(f'/users/{str(request_uuid1)}/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_profile_update_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.patch(
            f'/users/{str(request_uuid1)}/',
            {"first_name": "test1_upd"},
            format='json')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'first_name': 'test1_upd',
                    'patronymic': 'testovich1',
                    'surname': 'testov1'}
        self.assertEqual(processed_response, expected)

    def test_profile_update_negative(self):
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.patch(
            f'/users/{str(request_uuid1)}/',
            {"first_name": "test1_upd"},
            format='json')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.patch(
            f'/users/{str(request_uuid1)}/',
            {"first_name": "test1_upd"},
            format='json')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_profile_destroy_postive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.delete(f'/users/{str(request_uuid1)}/')
        self.assertEqual(response.status_code, 204)

    def test_profile_destroy_negative(self):
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.delete(f'/users/{str(request_uuid1)}/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.delete(f'/users/{str(request_uuid1)}/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_phone_create_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        user_profile_pk1 = UserProfile.objects.get(first_name='test1').pk
        response = self.api_client.post(f'/users/{str(request_uuid1)}/phones/', {
            'user_profile': user_profile_pk1,
            'phone': '5555',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'phone': '5555'}
        self.assertEqual(processed_response, expected)

    def test_phone_create_negative(self):
        request_uuid1 = self.profile1.uu_id
        user_profile_pk1 = UserProfile.objects.get(first_name='test1').pk
        response = self.api_client.post(f'/users/{str(request_uuid1)}/phones/', {
            'user_profile': user_profile_pk1,
            'phone': '5555',
        }, format='json')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.post(f'/users/{str(request_uuid1)}/phones/', {
            'user_profile': user_profile_pk1,
            'phone': '5555',
        }, format='json')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_phone_list_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid1)}/phones/')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = [{'phone': '1111'}, {'phone': '2222'}]
        self.assertEqual(processed_response, expected)

    def test_phone_list_negative(self):
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid1)}/phones/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.get(f'/users/{str(request_uuid1)}/phones/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_phone_retrieve_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        profile_uuid = self.profile1.uu_id
        phone_uuid = self.phone1.uu_id
        response = self.api_client.get(f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'phone': '1111'}
        self.assertEqual(processed_response, expected)

    def test_phone_retrieve_negative(self):
        profile_uuid = self.profile1.uu_id
        phone_uuid = self.phone1.uu_id
        response = self.api_client.get(f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.get(f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_phone_update_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        profile_uuid = self.profile1.uu_id
        phone_uuid = self.phone1.uu_id
        response = self.api_client.patch(
            f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/',
            {"phone": "1111_upd"},
            format='json')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'phone': '1111_upd'}
        self.assertEqual(processed_response, expected)

    def test_phone_update_negative(self):
        profile_uuid = self.profile1.uu_id
        phone_uuid = self.phone1.uu_id
        response = self.api_client.patch(
            f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/',
            {"phone": "1111_upd"},
            format='json')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.patch(
            f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/',
            {"phone": "1111_upd"},
            format='json')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_phone_destroy_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        profile_uuid = self.profile1.uu_id
        phone_uuid = self.phone1.uu_id
        response = self.api_client.delete(
            f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/')
        self.assertEqual(response.status_code, 204)

    def test_phone_destroy_negative(self):
        profile_uuid = self.profile1.uu_id
        phone_uuid = self.phone1.uu_id
        response = self.api_client.delete(
            f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.delete(
            f'/users/{str(profile_uuid)}/phones/{str(phone_uuid)}/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_address_create_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        user_profile_pk1 = UserProfile.objects.get(first_name='test1').pk
        response = self.api_client.post(f'/users/{str(request_uuid1)}/addresses/', {
            'user_profile': user_profile_pk1,
            'city': 'fourth city',
            'address': 'fourth address'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'city': 'fourth city', 'address': 'fourth address'}
        self.assertEqual(processed_response, expected)

    def test_address_create_negative(self):
        request_uuid1 = self.profile1.uu_id
        user_profile_pk1 = UserProfile.objects.get(first_name='test1').pk
        response = self.api_client.post(f'/users/{str(request_uuid1)}/addresses/', {
            'user_profile': user_profile_pk1,
            'city': 'fourth city',
            'address': 'fourth address'
        }, format='json')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.post(f'/users/{str(request_uuid1)}/addresses/', {
            'user_profile': user_profile_pk1,
            'city': 'fourth city',
            'address': 'fourth address'
        }, format='json')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_address_list_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid1)}/addresses/')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = [{'address': 'first address',
                     'city': 'first city'},
                    {'address': 'second address',
                     'city': 'second city'}]
        self.assertEqual(processed_response, expected)

    def test_address_list_negative(self):
        request_uuid1 = self.profile1.uu_id
        response = self.api_client.get(f'/users/{str(request_uuid1)}/addresses/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.get(f'/users/{str(request_uuid1)}/addresses/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_address_retrieve_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        profile_uuid = self.profile1.uu_id
        address_uuid = self.address1.uu_id
        response = self.api_client.get(f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'address': 'first address',
                    'city': 'first city'}
        self.assertEqual(processed_response, expected)

    def test_address_retrieve_negative(self):
        profile_uuid = self.profile1.uu_id
        address_uuid = self.address1.uu_id
        response = self.api_client.get(f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.get(f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_address_update_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        profile_uuid = self.profile1.uu_id
        address_uuid = self.address1.uu_id
        response = self.api_client.patch(
            f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/',
            {"city": "first city upd"},
            format='json')
        self.assertEqual(response.status_code, 200)
        t = uuidTest()
        processed_response = t.process_object_uuids(response.json())
        expected = {'address': 'first address',
                    'city': 'first city upd'}
        self.assertEqual(processed_response, expected)

    def test_address_update_negative(self):
        profile_uuid = self.profile1.uu_id
        address_uuid = self.address1.uu_id
        response = self.api_client.patch(
            f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/',
            {"city": "first city upd"},
            format='json')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.patch(
            f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/',
            {"city": "first city upd"},
            format='json')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)

    def test_address_destroy_positive(self):
        self.api_client.login(username='test_user1', password='password1')
        profile_uuid = self.profile1.uu_id
        address_uuid = self.address1.uu_id
        response = self.api_client.delete(
            f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/')
        self.assertEqual(response.status_code, 204)

    def test_address_destroy_negative(self):
        profile_uuid = self.profile1.uu_id
        address_uuid = self.address1.uu_id
        response = self.api_client.delete(
            f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/')
        self.assertEqual(response.status_code, 403)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), expected)

        self.api_client.login(username='test_user2', password='password2')
        response = self.api_client.delete(
            f'/users/{str(profile_uuid)}/addresses/{str(address_uuid)}/')
        self.assertEqual(response.status_code, 404)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.json(), expected)
