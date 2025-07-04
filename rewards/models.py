from django.db import models
from django.db.models import F


class Reward(models.Model):
    title = models.CharField(max_length=64)
    points_cost = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="rewards/")

    def decrement_stock(self) -> None:
        updated = Reward.objects.filter(pk=self.pk, stock__gt=0).update(
            stock=F("stock") - 1
        )
        if not updated:
            raise ValueError("Out of stock")

    def __str__(self) -> str:
        return self.title


class Redemption(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    reward = models.ForeignKey("rewards.Reward", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon_code = models.CharField(max_length=32, unique=True)