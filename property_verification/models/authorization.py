from django.db import models

from core.models import BaseModel
from property_verification.models.verification import PropertyVerification



class PropertyVerificationAuthorization(BaseModel):
    """
    Records the response submitted by the landlord or authorized
    representative for a property verification request.

    This is an immutable audit record of the representative's
    authorization decision.
    """

    class Decision(models.TextChoices):
        AUTHORIZED = (
            "authorized",
            "Authorized",
        )
        REJECTED = (
            "rejected",
            "Rejected",
        )

    verification = models.OneToOneField(
        PropertyVerification,
        on_delete=models.CASCADE,
        related_name="authorization",
    )

    decision = models.CharField(
        max_length=20,
        choices=Decision.choices,
        db_index=True,
    )

    availability_confirmed = models.BooleanField(
        default=False,
    )

    agent_authorized = models.BooleanField(
        default=False,
    )

    authorization_note = models.TextField(
        blank=True,
    )

    rejection_reason = models.TextField(
        blank=True,
    )

    responded_at = models.DateTimeField()

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-responded_at"]

        indexes = [
            models.Index(
                fields=[
                    "decision",
                    "-responded_at",
                ],
                name="prop_auth_decision_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.verification.submission} - "
            f"{self.get_decision_display()}"
        )