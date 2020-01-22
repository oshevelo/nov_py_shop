from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShipmentsList.as_view(), name='shipments'),
    path('<int:shipment_id>', views.ShipmentsDetail.as_view(), name='shipment_detail')
]
