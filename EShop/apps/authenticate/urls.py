from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    #path('register', registration_view, name='register'),
    path('', views.UserList.as_view(), name='user_list')
]
