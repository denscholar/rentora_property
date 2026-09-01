from django.db import models
from core.models import BaseModel
from property_verification.models.verification import PropertyVerification


class RepresentativeRole(models.TextChoices):
    LANDLORD = "landlord", "Landlord"
    LAWYER = "lawyer", "Lawyer"
    ESTATE_MANAGER = "estate_manager", "Estate Manager"
    AUTHORIZED_REPRESENTATIVE = (
        "authorized_representative",
        "Authorized Representative",
    )


class VerificationRepresentative(BaseModel):
    """
    Stores the landlord or authorized representative responsible
    for confirming that an agent is authorized to market a property.
    """

    verification = models.OneToOneField(
        PropertyVerification,
        on_delete=models.CASCADE,
        related_name="representative",
    )

    name = models.CharField(
        max_length=255,
    )

    role = models.CharField(
        max_length=40,
        choices=RepresentativeRole.choices,
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    organization_name = models.CharField(
        max_length=255,
        blank=True,
    )

    confirmed_identity = models.BooleanField(
        default=False,
    )

    confirmed_authority = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - " f"{self.get_role_display()}"
