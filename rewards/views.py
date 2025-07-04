import uuid
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Reward, Redemption
from .serializers import RewardSerializer, RedemptionSerializer
from points.services import spend_points


class RewardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reward.objects.filter(stock__gt=0)
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAuthenticated]


class RedemptionViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RedemptionSerializer

    def create(self, request, *args, **kwargs):
        reward_id = request.data["reward"]
        reward = Reward.objects.get(pk=reward_id)
        reward.decrement_stock()
        spend_points(request.user.id, reward.points_cost)
        redemption = Redemption.objects.create(
            user=request.user,
            reward=reward,
            coupon_code=uuid.uuid4().hex[:12].upper(),
        )
        return Response(
            RedemptionSerializer(redemption).data, status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        qs = Redemption.objects.filter(user=request.user)
        return Response(RedemptionSerializer(qs, many=True).data)