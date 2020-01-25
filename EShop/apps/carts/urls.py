from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartList.as_view(), name='cart_list'),
    path('<int:cart_id>/', views.CartDetail.as_view(), name='cart_detail'),

    path('item/', views.CartItemList.as_view(), name='cart_item_list'),
    path('item/<int:cart_item_id>/', views.CartItemDetail.as_view(), name='cart_item_detail'),
]



