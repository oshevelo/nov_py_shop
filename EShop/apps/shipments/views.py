from django.http import HttpResponse
from apps.shipments.models import Shipments

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .models import Shipments
from .serializers import ShipmentsSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class ShipmentsList(generics.ListCreateAPIView):
    queryset=Shipments.objects.all()
    serializer_class = ShipmentsSerializer
    pagination_class=LimitOffsetPagination


class ShipmentsDetail(generics.RetrieveUpdateDestroyAPIView):
        
        serializer_class=ShipmentsSerializer

        def get_object(self):
            obj=get_object_or_404(Shipments, pk=self.kwargs.get('shipments_id'))
            return obj
