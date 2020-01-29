from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .models import Shipment
from .serializers import ShipmentSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class ShipmentList(generics.ListCreateAPIView):
    queryset=Shipment.objects.all()
    serializer_class = ShipmentSerializer
    pagination_class=LimitOffsetPagination


class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
        
        serializer_class=ShipmentSerializer

        def get_object(self):
            obj=get_object_or_404(Shipments, pk=self.kwargs.get('shipments_id'))
            return obj
