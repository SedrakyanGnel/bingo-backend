from django.db import models


class Bin(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["active"])]
        verbose_name = "Recycling bin"
        verbose_name_plural = "Recycling bins"

    def __str__(self) -> str:
        return self.id