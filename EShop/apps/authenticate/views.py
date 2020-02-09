from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from django.contrib.auth.models import User
from apps.authenticate.serializers import RegistrationSerializer
'''
@api_view(['POST',])
def registration_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data = request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = "successfuly registrated new user"
			data['email'] = account.email
			data['username'] = account.username
		else:
			data = serializer.errors
		return Response(data)
'''
class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegistrationSerializer