from rest_framework import serializers
from .models import Bin


class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ("id", "latitude", "longitude", "active")
        read_only_fields = fields