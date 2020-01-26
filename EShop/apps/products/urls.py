from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductsList.as_view(), name='product_list'),
    path('<int:product_id>', views.ProductDetail.as_view(), name='product_detail'),

    path('sets', views.SetsList.as_view(), name='set_list'),
    path('sets/<int:set_id>', views.SetDetail.as_view(), name='set_detail'),
]
