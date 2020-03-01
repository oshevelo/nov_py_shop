from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient


class AuthenticationTest(TestCase):

	def setUp(self):
		self.api_client = APIClient()

	def test_user_registration(self):
		response = self.api_client.post('/authenticate/api/v1/accounts/register/',
			{
			    "username": "test_username",
			    "first_name": "test_first_name",
			    "last_name": "test_last_name",
			    "email": "test_email_address@gmail.com",
			    "password": "test_passwordhardpasswordveryhard1231321312KkKkKkKk",
			    "password_confirm": "test_passwordhardpasswordveryhard1231321312KkKkKkKk",
			}, format='json')

		self.assertEqual(response.status_code, 201)
		User.objects.get(username='test_username',first_name='test_first_name',last_name='test_last_name') 

	def test_user_login(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user.save()

		response = self.api_client.post('/authenticate/api-auth/login/',
			{
				"username": "john",
				"password": "lennon@thebeatles.com",
			}, format='json')

		self.assertEqual(response.status_code, 200)