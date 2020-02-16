from django.contrib.auth.models import User, Group
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'groups': reverse('group-list', request=request),
    })


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = User
    serializer_class = UserSerializer
    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

class GroupList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    queryset = Group.objects.all()
    model = Group
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get('pk')) 
    model = Group
    serializer_class = GroupSerializer