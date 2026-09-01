from django.conf import settings
from django.db import models

from core.models import BaseModel
from properties.models.property.submission import PropertySubmission


class PropertyVerification(BaseModel):
    """
    Represents the SheltaMe verification workflow for a property
    submission.

    A property must receive authorization from the landlord or
    authorized representative before SheltaMe can verify it.
    """

    class EmailStatus(models.TextChoices):
        NOT_SENT = "not_sent", "Not Sent"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        AUTHORIZATION_SENT = "authorization_sent", "Authorization Sent"
        AUTHORIZED = "authorized", "Authorized"
        UNDER_REVIEW = "under_review", "Under Review"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"
        

    submission = models.OneToOneField(  
        PropertySubmission,
        on_delete=models.CASCADE,
        related_name="verification",
    )

    status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )

    token_hash = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
    )
    email_status = models.CharField(
        max_length=20,
        choices=EmailStatus.choices,
        default=EmailStatus.NOT_SENT,
        db_index=True,
    )

    email_sent_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    email_provider_id = models.CharField(
        max_length=255,
        blank=True,
    )

    email_error = models.TextField(
        blank=True,
    )

    token_expires_at = models.DateTimeField()

    authorization_sent_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    authorized_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    verified_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    rejected_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    rejection_reason = models.TextField(
        blank=True,
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="property_verifications_reviewed",
    )

    review_note = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["status", "-created_at"],
                name="prop_ver_status_created_idx",
            ),
            models.Index(
                fields=["token_expires_at"],
                name="prop_ver_token_expiry_idx",
            ),
        ]

    def __str__(self):
        return f"{self.submission} - " f"{self.get_status_display()}"
