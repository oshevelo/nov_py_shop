from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from apps.users import views as usv

api_urlpatterns = [path('accounts/', include('rest_registration.api.urls')),]

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^groups/$', views.GroupList.as_view(), name='group-list'),
    url(r'^groups/(?P<pk>\d+)/$', views.GroupDetail.as_view(), name='group-detail'),
    url(r'^oauth2/', include('social_django.urls', namespace='social')),
    path('api/v1/', include(api_urlpatterns)),
    #rest_registration registration view.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #rest_framework login view.
]