from django.db import models

from core.models import BaseModel


class VerificationDocumentType(models.TextChoices):
    AUTHORIZATION_LETTER = (
        "authorization_letter",
        "Authorization Letter",
    )

    OWNERSHIP_DOCUMENT = (
        "ownership_document",
        "Ownership Document",
    )

    LAWYER_DOCUMENT = (
        "lawyer_document",
        "Lawyer Document",
    )

    OTHER = "other", "Other"


class PropertyVerificationDocument(BaseModel):
    """
    Stores documentation submitted by the landlord or representative
    during property verification.
    """

    verification = models.ForeignKey(
        "property_verification.PropertyVerification",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=40,
        choices=VerificationDocumentType.choices,
    )

    public_id = models.CharField(
        max_length=500,
        unique=True,
    )

    secure_url = models.URLField(
        max_length=1000,
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True,
    )

    content_type = models.CharField(
        max_length=100,
        blank=True,
    )

    file_size = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )

    uploaded_by_name = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_document_type_display()} - " f"{self.verification}"
