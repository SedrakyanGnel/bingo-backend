from rest_framework import viewsets, permissions
from .serializers import BalanceSerializer


class BalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return [self.request.user]        # dummy iterable