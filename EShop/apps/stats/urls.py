from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.StatCreate.as_view(), name='stat_create'),
]
