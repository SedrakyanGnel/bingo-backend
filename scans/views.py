# scans/views.py
from rest_framework import mixins, parsers, permissions, status, viewsets
from rest_framework.response import Response

from .models import ScanEvent
from .serializers import ScanCreateSerializer, ScanEventSerializer


class ScanEventViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    REST entry-point for scan events.

    • POST multipart (bin, image) → stores photo, enqueues AI classification.  
    • GET  → list current user’s scans (admin sees all).  
    • GET /{id}/ → retrieve single scan record.
    """

    queryset = ScanEvent.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    # ──────────────────────────────────────────────────────────────────────────
    # Serialiser routing
    # ──────────────────────────────────────────────────────────────────────────
    def get_serializer_class(self):
        return ScanCreateSerializer if self.action == "create" else ScanEventSerializer

    # ──────────────────────────────────────────────────────────────────────────
    # Query filtering
    # ──────────────────────────────────────────────────────────────────────────
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    # ──────────────────────────────────────────────────────────────────────────
    # Response payload for create
    # ──────────────────────────────────────────────────────────────────────────
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scan_event = serializer.save()  # ScanCreateSerializer -> create_scan_with_photo
        return Response({"id": scan_event.id}, status=status.HTTP_201_CREATED)