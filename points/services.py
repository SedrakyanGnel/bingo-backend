from django.db.models import Sum
from .models import PointTransaction


def get_balance(user_id: int) -> int:
    return (
        PointTransaction.objects.filter(user_id=user_id)
        .aggregate(total=Sum("delta"))
        .get("total")
        or 0
    )


def add_points(user_id: int, amount: int, **relations) -> None:
    PointTransaction.objects.create(
        user_id=user_id, delta=amount, kind=PointTransaction.EARN, **relations
    )


def spend_points(user_id: int, amount: int, **relations) -> None:
    balance = get_balance(user_id)
    if balance < amount:
        raise ValueError("Not enough points")
    PointTransaction.objects.create(
        user_id=user_id, delta=-amount, kind=PointTransaction.SPEND, **relations
    )