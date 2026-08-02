from django.db import models

from .base import LookupBaseModel


# =====================================================
# PROPERTY PURPOSE
# =====================================================
class PropertyPurpose(LookupBaseModel):
    code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )

    allow_viewing_booking = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name",]