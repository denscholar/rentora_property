from django.db import models

from .base import LookupBaseModel
from .amenity_category import AmenityCategory


# =====================================================
# AMENITY
# =====================================================
class Amenity(LookupBaseModel):
    category = models.ForeignKey(
        AmenityCategory,
        on_delete=models.SET_NULL,
        related_name="amenities",
        blank=True,
        null=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Amenities"

        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_amenity_per_category",
            )
        ]