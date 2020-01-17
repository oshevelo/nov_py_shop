from django.urls import path

from . import views


urlpatterns = [
    path('products/', views.ProductsList.as_view(), name='product_list'),
    path('products/<int:product_id>', views.ProductsList.as_view(), name='product_list'),
]
