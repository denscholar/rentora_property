from django.db import models
from .base import LookupBaseModel


# =====================================================
# AMENITY CATEGORY
# =====================================================
class AmenityCategory(LookupBaseModel):
    code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Amenity Categories"