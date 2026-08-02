# =====================================================
# PROPERTY SUBMISSION MODEL
# =====================================================

from django.conf import settings
from django.db import models

from core.models import BaseModel, GeoLocationMixin, SoftArchiveMixin
from locations.models import Area
from properties.models.lookups import PropertyPurpose, PropertyType
from properties.models.lookups.amenity import Amenity
from properties.models.lookups.furnishing_status import FurnishingStatus
from properties.models.lookups.property_condition import PropertyCondition


class PaymentFrequency(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    BIANNUALLY = "biannually", "Biannually"
    ANNUALLY = "annually", "Annually"
    ONE_TIME = "one_time", "One Time"


class SizeUnit(models.TextChoices):
    SQUARE_METERS = "sqm", "Square Metres"
    SQUARE_FEET = "sqft", "Square Feet"
    ACRES = "acres", "Acres"
    HECTARES = "hectares", "Hectares"
    PLOTS = "plots", "Plots"


# =====================================================
# PROPERTY SUBMISSION
# =====================================================
class PropertySubmission(BaseModel, GeoLocationMixin, SoftArchiveMixin):
    """
    Stores property information submitted by an agent, landlord,
    or admin before it becomes a verified Property.

    This protects the main Property table from fake, duplicate,
    incomplete, or unverified records.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        UNDER_REVIEW = "under_review", "Under Review"
        DUPLICATE_FOUND = "duplicate_found", "Duplicate Found"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        MORE_INFORMATION_REQUIRED = (
            "more_information_required",
            "More Information Required",
        )

    class Source(models.TextChoices):
        AGENT = "agent", "Agent"
        LANDLORD = "landlord", "Landlord"
        ADMIN = "admin", "Admin"

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="property_submissions",
    )

    source = models.CharField(max_length=30, choices=Source.choices, editable=False)

    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.PROTECT,
        related_name="submissions",
        blank=True,
        null=True,
    )

    purpose = models.ForeignKey(
        PropertyPurpose,
        on_delete=models.PROTECT,
        related_name="submissions",
        blank=True,
        null=True,
    )
    property_condition = models.ForeignKey(
        PropertyCondition,
        on_delete=models.PROTECT,
        related_name="submissions",
        blank=True,
        null=True,
    )
    furnishing_status = models.ForeignKey(
        FurnishingStatus,
        on_delete=models.PROTECT,
        related_name="submissions",
        blank=True,
        null=True,
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="property_submissions",
        blank=True,
        null=True,
    )
    amenities = models.ManyToManyField(
        Amenity,
        related_name="property_submissions",
        blank=True,
    )
    size_unit = models.CharField(
        max_length=20,
        choices=SizeUnit.choices,
        default=SizeUnit.SQUARE_METERS,
    )
    land_size = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Land size expressed in the selected unit.",
    )

    building_size = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Building or floor size expressed in the selected unit.",
    )
    payment_frequency = models.CharField(
        max_length=20,
        default=PaymentFrequency.ANNUALLY,
        choices=PaymentFrequency.choices,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    landmark = models.CharField(
        max_length=255,
        blank=True,
        help_text="Private address. Not shown publicly before booking.",
    )

    street_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Private address. Not shown publicly before booking.",
    )

    bedrooms = models.PositiveIntegerField(default=0)

    bathrooms = models.PositiveIntegerField(default=0)

    toilets = models.PositiveIntegerField(default=0)

    parking_spaces = models.PositiveIntegerField(default=0)

    proposed_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        blank=True,
        null=True,
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

    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    # possible_duplicate_property = models.ForeignKey(
    #     "properties.Property",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="duplicate_submissions",
    # )

    duplicate_similarity_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Similarity percentage between 0 and 100.",
    )

    review_note = models.TextField(
        blank=True,
        null=True,
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviewed_property_submissions",
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    floors = models.PositiveIntegerField(
        default=0,
    )

    units_available = models.PositiveIntegerField(
        default=1,
    )

    year_built = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    is_new_build = models.BooleanField(
        default=False,
    )

    is_serviced = models.BooleanField(
        default=False,
    )

    is_negotiable = models.BooleanField(
        default=False,
    )

    available_from = models.DateField(
        blank=True,
        null=True,
    )

    minimum_stay = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Minimum stay measured using the payment frequency.",
    )

    # approved_property = models.ForeignKey(
    #     "properties.Property",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="source_submissions",
    # )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["status", "-created_at"],
                name="submission_status_created_idx",
            ),
            models.Index(
                fields=["submitted_by", "status"],
                name="submission_user_status_idx",
            ),
            models.Index(
                fields=["area", "property_type", "purpose", "bedrooms"],
                name="sub_duplicate_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(duplicate_similarity_score__isnull=True)
                    | models.Q(
                        duplicate_similarity_score__gte=0,
                        duplicate_similarity_score__lte=100,
                    )
                ),
                name="submission_similarity_score_0_100",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(proposed_price__isnull=True)
                    | models.Q(proposed_price__gte=0)
                ),
                name="submission_proposed_price_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(service_charge__gte=0),
                name="submission_service_charge_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(caution_fee__gte=0),
                name="submission_caution_fee_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(legal_fee__gte=0),
                name="submission_legal_fee_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(agency_fee__gte=0),
                name="submission_agency_fee_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(land_size__isnull=True) | models.Q(land_size__gte=0)
                ),
                name="submission_land_size_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(building_size__isnull=True)
                    | models.Q(building_size__gte=0)
                ),
                name="submission_building_size_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(year_built__isnull=True) | models.Q(year_built__gte=1800)
                ),
                name="submission_year_built_reasonable_minimum",
            ),
        ]

    def __str__(self):
        title = self.title or "Untitled draft"
        return f"{title} - {self.get_status_display()}"
