from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartList.as_view(), name='cart_list'),
    path('<uuid:cart_uuid>/', views.CartDetail.as_view(), name='cart_detail'),

    path('<uuid:cart_uuid>/item/', views.CartItemList.as_view(), name='cart_item_list'),
    path('<uuid:cart_uuid>/item/<uuid:cart_item_uuid>/', views.CartItemDetail.as_view(), name='cart_item_detail'),
]



