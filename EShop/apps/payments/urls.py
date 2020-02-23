from django.urls import path
from . import views


urlpatterns = [
    path('', views.PaymentList.as_view(), name='PaymentList'),
    path('id/<int:id>/', views.PaymentDetail.as_view(), name='PaymentDetails'),
]
