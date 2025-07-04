from rest_framework import viewsets, permissions
from .models import Bin
from .serializers import BinSerializer


class BinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bin.objects.filter(active=True)
    serializer_class = BinSerializer
    permission_classes = [permissions.AllowAny]   # public map