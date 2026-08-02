from django.db import models

from .base import LookupBaseModel


# =====================================================
# PROPERTY CONDITION
# =====================================================
class PropertyCondition(LookupBaseModel):
    """
    Describes the physical condition of a property.

    Examples:
    - Newly Built
    - Newly Renovated
    - Fairly Used
    - Old
    - Needs Renovation
    - Off Plan
    """

    code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Property Condition"
        verbose_name_plural = "Property Conditions"