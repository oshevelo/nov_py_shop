from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from apps.stats.serializers import StatSerializer


class StatCreate(generics.CreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = StatSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(user=self.request.user)
