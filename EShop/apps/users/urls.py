from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfileList.as_view(), name='user_profile_list'),
    path('<uuid:user_profile_uu_id>/', views.UserProfileDetail.as_view(),
         name='user_profile'),

    path('<uuid:user_profile_uu_id>/addresses/',
         views.UserAddressList.as_view(), name='user_adress_list'),
    path('<uuid:user_profile_uu_id>/addresses/<uuid:user_address_uu_id>/',
         views.UserAddressDetail.as_view(), name='user_address'),

    path('<uuid:user_profile_uu_id>/phones/',
         views.UserPhoneList.as_view(), name='user_phone_list'),
    path('<uuid:user_profile_uu_id>/phones/<uuid:user_phone_uu_id>/',
         views.UserPhoneDetail.as_view(), name='user_phone'),
]
