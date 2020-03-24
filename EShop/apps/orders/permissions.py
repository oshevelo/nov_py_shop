from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Order
from apps.shipments.models import Shipment


class OrderEditPermission(BasePermission):
    def has_permission(self, request, view):
        order = get_object_or_404(Order, pub_id=view.kwargs.get('order_uuid'), user=request.user)
        return order.is_editable

        
class AddOrderItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            order = get_object_or_404(Order, pub_id=view.kwargs.get('order_uuid'), user=request.user)
            return not order.max_orderitems
        return True
        
        
class ReadOnlyMethod(BasePermission):
    def has_permission(self, request, view):
        read_only_methods=('GET', 'OPTIONS', 'HEAD')
        return request.method in read_only_methods
        
        
class ShipmentExists(BasePermission):
    def has_permission(self, request, view):
        selected_order = get_object_or_404(Order, pub_id=view.kwargs.get('order_uuid'), user=request.user)
        return not Shipment.objects.filter(order=selected_order) 