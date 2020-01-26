from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShipmentList.as_view(), name='shipment'),
    path('<int:shipment_tracking_number>', views.ShipmentDetail.as_view(), name='shipment_detail')
]
