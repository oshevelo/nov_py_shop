from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('<int:user_id>/', views.UserDetail.as_view(), name='user'),

    path('address/', views.UserAddressList.as_view(), name='user_adress_list'),
    path('address/<int:user_address_id>/',
         views.UserAddressDetail.as_view(), name='user_address'),

    path('phones/', views.UserPhoneList.as_view(), name='user_phone_list'),
    path('phones/<int:user_phone_id>/',
         views.UserPhoneDetail.as_view(), name='user_phone'),
]
