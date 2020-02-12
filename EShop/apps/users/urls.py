from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfileList.as_view(), name='user_profile_list'),
    path('<uuid:user_profile_uu_id>/', views.UserProfileDetail.as_view(),
         name='user_profile'),

    path('address/', views.UserAddressList.as_view(), name='user_adress_list'),
    path('address/<uuid:user_address_uu_id>/',
         views.UserAddressDetail.as_view(), name='user_address'),

    path('phones/', views.UserPhoneList.as_view(), name='user_phone_list'),
    path('phones/<uuid:user_phone_uu_id>/',
         views.UserPhoneDetail.as_view(), name='user_phone'),
]
