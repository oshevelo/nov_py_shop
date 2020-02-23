from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from apps.users import views as usv

api_urlpatterns = [path('accounts/', include('rest_registration.api.urls')),]

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

    #url(r'^social-auth/$',views.SocialSignUp.as_view({"post": "create", "get": "list"}), name='api-social-auth-register')
   	#google registration view (in development :D )

    path('api/v1/', include(api_urlpatterns)),
    #rest default registration view. Access by this url
    #http://127.0.0.1:8000/authenticate/api/v1/accounts/register/
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #rest default login view. Access by this url
    #http://127.0.0.1:8000/authenticate/api-auth/login/

]

# Format suffixe
#urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

