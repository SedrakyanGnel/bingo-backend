from django.db import models


class PointTransaction(models.Model):
    EARN, SPEND = "E", "S"
    KIND_CHOICES = [(EARN, "earn"), (SPEND, "spend")]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    delta = models.SmallIntegerField()
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)
    related_scan = models.ForeignKey(
        "scans.ScanEvent", null=True, blank=True, on_delete=models.SET_NULL
    )
    related_redemption = models.ForeignKey(
        "rewards.Redemption", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]
        ordering = ["-created_at"]