from rest_framework import serializers
from points.services import get_balance


class BalanceSerializer(serializers.Serializer):
    balance = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        return {"balance": get_balance(instance.id)}