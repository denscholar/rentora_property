from django.conf import settings
from django.db import models
from accounts.models import CustomUser
from core.models import BaseModel
from properties.models.property.property_group import PropertyGroup



class PropertyRepresentation(BaseModel):
    """
    Represents an agent's relationship with a canonical PropertyGroup.
    Multiple agents can represent the same physical property.
    Example:

        PropertyGroup #42
            ├── Agent A
            ├── Agent B
            └── Agent C

    Each agent may have different pricing, description, fees,
    availability and inspection arrangements.
    """

    class Status(models.TextChoices):
        ACTIVE = (
            "active",
            "Active",
        )
        SUSPENDED = (
            "suspended",
            "Suspended",
        )
        INACTIVE = (
            "inactive",
            "Inactive",
        )

    # =====================================================
    # PROPERTY
    # =====================================================

    property_group = models.ForeignKey(
        PropertyGroup,
        on_delete=models.CASCADE,
        related_name="representations",
    )

    # =====================================================
    # AGENT
    # =====================================================

    agent = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="property_representations",
    )

    # =====================================================
    # SOURCE SUBMISSION
    # =====================================================

    submission = models.OneToOneField(
        "properties.PropertySubmission",
        on_delete=models.PROTECT,
        related_name="representation",
    )

    # =====================================================
    # AGENT-SPECIFIC LISTING INFORMATION
    # =====================================================

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    # =====================================================
    # PRICING
    # =====================================================

    proposed_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        blank=True,
        null=True,
    )

    payment_frequency = models.CharField(
        max_length=20,
        blank=True,
    )

    service_charge = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    caution_fee = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    legal_fee = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    agency_fee = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    is_negotiable = models.BooleanField(
        default=False,
    )

    # =====================================================
    # AVAILABILITY
    # =====================================================

    available_from = models.DateField(
        blank=True,
        null=True,
    )

    minimum_stay = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # =====================================================
    # REPRESENTATION STATUS
    # =====================================================

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    # =====================================================
    # INSPECTION
    # =====================================================

    inspection_enabled = models.BooleanField(
        default=True,
    )

    # =====================================================
    # VERIFICATION
    # =====================================================

    verified_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "property_group",
                    "agent",
                ],
                name="unique_property_group_agent",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "property_group",
                    "status",
                ],
                name="property_repr_pro_status_idx",
            ),
            models.Index(
                fields=[
                    "agent",
                    "status",
                ],
                name="property_repr_agent_status_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.agent} - "
            f"{self.property_group}"
        )