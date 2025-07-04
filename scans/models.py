from django.db import models
from django.utils import timezone


class ScanEvent(models.Model):
    # ─── Hard-coded trash categories ──────────────────────────────────────────
    TRASH_PLASTIC  = "plastic"
    TRASH_METAL    = "metal"
    TRASH_GLASS    = "glass"
    TRASH_PAPER    = "paper"
    TRASH_UNSORTED = "unsorted"

    TRASH_CHOICES = [
        (TRASH_PLASTIC,  "Plastic"),
        (TRASH_METAL,    "Metal"),
        (TRASH_GLASS,    "Glass"),
        (TRASH_PAPER,    "Paper"),
        (TRASH_UNSORTED, "Unsorted"),
    ]

    # ─── Fields ───────────────────────────────────────────────────────────────
    user        = models.ForeignKey("users.User", on_delete=models.CASCADE)
    bin         = models.ForeignKey("bins.Bin",  on_delete=models.CASCADE)
    image       = models.ImageField(upload_to="scans/%Y/%m/%d/")
    trash_type  = models.CharField(
        max_length=10, choices=TRASH_CHOICES, null=True, blank=True
    )
    confidence  = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes  = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["bin",  "created_at"]),
        ]
        ordering = ["-created_at"]

    # Helper: did the user scan in the last <window>
    @classmethod
    def recent_for_user(cls, user_id, window):
        return cls.objects.filter(
            user_id=user_id,
            created_at__gte=timezone.now() - window,
        ).exists()