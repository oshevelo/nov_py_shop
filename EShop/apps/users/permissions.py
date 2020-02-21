from rest_framework.permissions import BasePermission
from apps.users.models import UserProfile
from django.contrib.auth.models import User


class UserProfileEditPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return False
        try:
            profile = UserProfile.objects.get(
                uu_id=view.kwargs['user_profile_uu_id'],
                user=request.user)
            return profile.pk == request.data['user_profile']
        except Exception:
            print('No permission')
            return False


class RequestIsList(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'
