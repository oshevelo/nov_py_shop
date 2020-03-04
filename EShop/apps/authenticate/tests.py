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

	def test_user_django_login(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user.save()

		response = self.api_client.post('/authenticate/api-auth/login/',
			{
				"username": "john",
				"password": "lennon@thebeatles.com",
			}, format='json')

		self.assertEqual(response.status_code, 200)

	def test_password_confirm(self):
		response = self.api_client.post('/authenticate/api/v1/accounts/register/',
			{
			    "username": "test_username",
			    "first_name": "test_first_name",
			    "last_name": "test_last_name",
			    "email": "test_email_address@gmail.com",
			    "password": "test_passwordhardpasswordveryhard1231321312KkKkKkKk",
			    "password_confirm": "erlkjhflsfjhsadfhasdkj",
			}, format='json')

		self.assertEqual(response.status_code, 400)

	def test_username_is_occupied(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

		response = self.api_client.post('/authenticate/api/v1/accounts/register/',
			{
			    "username": "john",
			    "first_name": "test_first_name",
			    "last_name": "test_last_name",
			    "email": "test_email_address@gmail.com",
			    "password": "test_passwordhardpasswordveryhard1231321312KkKkKkKk",
			    "password_confirm": "test_passwordhardpasswordveryhard1231321312KkKkKkKk",
			}, format='json')

		self.assertEqual(response.status_code, 400)

	'''
	"password": [
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric."
	'''

	def test_too_short_password(self):
		response = self.api_client.post('/authenticate/api/v1/accounts/register/',
			{
			    "username": "test_username",
			    "first_name": "test_first_name",
			    "last_name": "test_last_name",
			    "email": "test_email_address@gmail.com",
			    "password": "1g2g3g5",
			    "password_confirm": "1g2g3g5",
			}, format='json')

		self.assertEqual(response.status_code, 400)

	def test_numeric_password(self):
		response = self.api_client.post('/authenticate/api/v1/accounts/register/',
			{
			    "username": "test_username",
			    "first_name": "test_first_name",
			    "last_name": "test_last_name",
			    "email": "test_email_address@gmail.com",
			    "password": "63298762359736598659386598653298652398632896234962346723596",
			    "password_confirm": "63298762359736598659386598653298652398632896234962346723596",
			}, format='json')

		self.assertEqual(response.status_code, 400)

	def test_too_common(self):

		with open("common_passwords.txt", "r") as file:
			lines = file.readlines()
		for i in range(len(lines)):
			lines[i] = lines[i].rstrip('\n')
			response = self.api_client.post('/authenticate/api/v1/accounts/register/',
			{
			    "username": "test_username",
			    "first_name": "test_first_name",
			    "last_name": "test_last_name",
			    "email": "test_email_address@gmail.com",
			    "password": lines[i],
			    "password_confirm": lines[i],
			}, format='json')

			self.assertEqual(response.status_code, 400)