from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from .models import Order

class OrderEditPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            order = get_object_or_404(Order, pub_id=view.kwargs.get('order_uuid'), user=request.user)
            return order.is_editable

        
class AddOrderItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            order = get_object_or_404(Order, pub_id=view.kwargs.get('order_uuid'), user=request.user)
            return not order.max_orderitems
        return True
        