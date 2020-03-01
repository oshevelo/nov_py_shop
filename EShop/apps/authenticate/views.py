from django.contrib.auth.models import User, Group
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser


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
        'user_profile': reverse('user_profile_list', request=request),
    })


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    permission_classes = [IsAdminUser]
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