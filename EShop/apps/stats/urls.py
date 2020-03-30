from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.StatCreate.as_view(), name='stat_create'),
    path('last_seen_products/', views.LastSeenProducts.as_view(),
         name='last_seen_products')
]
