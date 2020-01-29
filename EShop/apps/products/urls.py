from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductsList.as_view(), name='product_list'),
    path('<int:product_id>', views.ProductDetail.as_view(), name='product_detail'),

    path('kits/', views.KitsList.as_view(), name='set_list'),
    path('kits/<int:kit_id>', views.KitDetail.as_view(), name='set_detail'),
]
