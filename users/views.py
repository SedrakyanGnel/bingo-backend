from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserPublicSerializer

User = get_user_model()


class MeViewSet(viewsets.ReadOnlyModelViewSet):
    """ /api/me – single-record endpoint for current user """
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)