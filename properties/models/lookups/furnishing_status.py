from django.db import models

from .base import LookupBaseModel


# =====================================================
# FURNISHING STATUS
# =====================================================
class FurnishingStatus(LookupBaseModel):
    """
    Describes the furnishing state of a property.

    Examples:
    - Unfurnished
    - Semi Furnished
    - Fully Furnished
    - Serviced
    """

    code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Furnishing Status"
        verbose_name_plural = "Furnishing Statuses"