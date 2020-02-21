from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from apps.users.models import UserProfile


class UserProfileEditPermission(BasePermission):
    def has_permission(self, request, view):
        profile = get_object_or_404(UserProfile,
                                    uu_id=view.kwargs['user_profile_uu_id'],
                                    user=request.user)
        return True


class RequestIsList(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'
