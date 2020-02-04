from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('<str:order_uuid>', views.OrderDetail.as_view(), name='order_details'),
    path('item/', views.OrderItemList.as_view(), name='orderitem_list'),
    path('item/<str:orderitem_uuid>/', views.OrderItemDetail.as_view(), name='orderitem_details'),
]
