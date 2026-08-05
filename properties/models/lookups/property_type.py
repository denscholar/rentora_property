from django.db import models

from .base import LookupBaseModel


# =====================================================
# PROPERTY TYPE
# =====================================================
class PropertyType(LookupBaseModel):
    code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["display_order", "name"]