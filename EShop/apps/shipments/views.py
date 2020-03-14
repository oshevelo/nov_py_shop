from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .models import Shipment
from .serializers import ShipmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ShipmentList(generics.ListCreateAPIView):
    serializer_class = ShipmentSerializer
    pagination_class=LimitOffsetPagination
    permission_classes=(IsAuthenticated,)
    
    def get_queryset(self):
        return Shipment.objects.filter(order__user=self.request.user)



class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
        
        serializer_class=ShipmentSerializer

        def get_object(self):
            obj=get_object_or_404(
            Shipment, 
            uuid=self.kwargs.get('shipment_uuid'), 
            order__user=self.request.user)
            return obj
