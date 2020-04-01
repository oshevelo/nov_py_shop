from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from apps.stats.serializers import StatSerializer, LastSeenProductsSerializer
from apps.users.models import UserProfile


class StatCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StatSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(user=self.request.user)


class LastSeenProducts(generics.RetrieveAPIView):
    serializer_class = LastSeenProductsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
