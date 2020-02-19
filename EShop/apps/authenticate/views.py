from django.contrib.auth.models import User, Group
#from django.contrib.auth import User as NotModelUser
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer
#from social_auth.backends.google import GOOGLEAPIS_PROFILE, googleapis_profile
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
#from social_auth.backends import get_backend
#from .serializers import UserRegisterSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
#permissoin class which allow user to only get content

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'groups': reverse('group-list', request=request),
        'rest_registration': reverse('rest_registration:register', request=request),
        'rest_framework_login': reverse('rest_framework:login', request=request),
        'rest_registration_login': reverse('rest_registration:login' ,request=request),
        'user_profile': reverse('user_profile_list', request=request),
    })


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    permission_classes = [IsAdminUser]
    #permission which works for admins and stuff users
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    permission_classes = [IsAdminUser]
    model = User
    serializer_class = UserSerializer
    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

class GroupList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    model = Group
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    permission_classes = [IsAdminUser]
    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get('pk')) 
    model = Group
    serializer_class = GroupSerializer

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\//\/\/\/\/\/\\/\/
'''
class SocialSignUp(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	permission_classes = (AllowAny,)
	throttle_classes = (AnonRateThrottle, )
	def create(self, request, *args, **kwargs):
		redirect = request.path
		try:
			provider = request.DATA[‘provider’]
			access_token = request.DATA[‘access_token’]
		except KeyError:
			return Response({‘success’: False, ‘detail’: “‘provider’ and ‘access_token’ are required parameters”},
			status=status.HTTP_400_BAD_REQUEST)
		backend = get_backend(provider, request, redirect)
		request.social_auth_backend = backend
		if access_token:
			try:
				if provider == “google-oauth2”:
					test_response = googleapis_profile(GOOGLEAPIS_PROFILE, access_token)
				if test_response is None:
					return Response({‘success’: False, ‘detail’: “bad access_token”}, status=status.HTTP_400_BAD_REQUEST)
				user = backend.do_auth(access_token, expires=None, *args, **kwargs)
				my_user = User.objects.get(user=user)
				user_serializer = UserRegisterSerializer(my_user)
				return Response({‘success’: True, ‘detail’: user_serializer.data})
			except Exception as e:
				return Response({‘success’: False, ‘detail’: e},
				status=status.HTTP_400_BAD_REQUEST)'''