from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from apps.users import views as usv


urlpatterns = [
    url(r'^$', views.api_root),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    #url(r'^users/$', usv.UserProfileList.as_view(), name='user-list'),	
    #user app user list view

    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-detail'),
    #url(r'^users/(?P<user_profile_uu_id>\d+)/$', usv.UserProfileDetail.as_view(), name='user-detail'),
    #user app profile detail view

    url(r'^groups/$', views.GroupList.as_view(), name='group-list'),
    url(r'^groups/(?P<pk>\d+)/$', views.GroupDetail.as_view(), name='group-detail'),
]
'''
urlpatterns = [
    path('', views.api_root),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:user_id>/', views.UserDetail.as_view(), name='user-detail'),
    path('groups/', views.GroupList.as_view(), name='group-list'),
    path('groups/<int:group_id>/', views.GroupDetail.as_view(), name='group-detail'),
]
'''

# Format suffixe
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]