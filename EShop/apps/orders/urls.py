from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('<str:order_uuid>', views.OrderDetail.as_view(), name='order_details'),
    path('<str:order_uuid>/item/', views.OrderItemList.as_view(), name='orderitem_list'),
    path('<str:order_uuid>/item/<str:orderitem_uuid>/', views.OrderItemDetail.as_view(), name='orderitem_details'),
    path('<str:order_uuid>/attach_shipment', views.AttachShipment.as_view(), name='attach_shipment'),
]
