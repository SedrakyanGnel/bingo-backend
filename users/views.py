from rest_framework import viewsets, permissions, generics, status
from django.contrib.auth import get_user_model
from .serializers import UserPublicSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []  # AllowAny

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )

class MeViewSet(viewsets.ReadOnlyModelViewSet):
    """ /api/me – single-record endpoint for current user """
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)