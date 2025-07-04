from rest_framework import serializers
from .models import Reward, Redemption
from points.services import spend_points

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ("id", "title", "points_cost", "stock", "image")
        read_only_fields = fields


class RedemptionSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(read_only=True)

    class Meta:
        model = Redemption
        fields = ("id", "reward", "created_at", "coupon_code")
        read_only_fields = fields