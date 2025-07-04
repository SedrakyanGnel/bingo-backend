from rest_framework import serializers

from .models import ScanEvent
from .services import create_scan_with_photo


class ScanEventSerializer(serializers.ModelSerializer):
    """for GET-requests (list / retrieve)."""

    class Meta:
        model = ScanEvent
        fields = [
            "id",
            "user",
            "bin",
            "image",
            "trash_type",
            "confidence",
            "created_at",
        ]
        read_only_fields = fields


class ScanCreateSerializer(serializers.Serializer):
    """for POST multipart (bin + image)."""

    bin = serializers.CharField(max_length=32)
    image = serializers.ImageField()

    def create(self, validated_data):
        return create_scan_with_photo(
            user_id=self.context["request"].user.id,
            bin_id=validated_data["bin"],
            image_file=validated_data["image"],
        )