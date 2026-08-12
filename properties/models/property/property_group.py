from django.db import models

from core.models import (
    BaseModel,
    GeoLocationMixin,
    SoftArchiveMixin,
)

from locations.models import Area

from properties.models.lookups import (
    PropertyPurpose,
    PropertyType,
)

from properties.models.lookups.amenity import Amenity
from properties.models.lookups.furnishing_status import FurnishingStatus
from properties.models.lookups.property_condition import PropertyCondition


class PropertyGroup(BaseModel, GeoLocationMixin, SoftArchiveMixin):
    """
    Represents the canonical physical identity of a property.

    Multiple agents can represent the same PropertyGroup through
    PropertyRepresentation records.

    A PropertyGroup represents ONE physical property or unit,
    not an individual agent's listing.
    """

    class PropertyCategory(models.TextChoices):
        STANDALONE_HOUSE = (
            "standalone_house",
            "Standalone House",
        )
        APARTMENT = (
            "apartment",
            "Apartment",
        )
        ESTATE_PROPERTY = (
            "estate_property",
            "Estate Property",
        )
        ROOM = (
            "room",
            "Room",
        )
        COMMERCIAL = (
            "commercial",
            "Commercial Property",
        )
        LAND = (
            "land",
            "Land",
        )

    # =====================================================
    # CLASSIFICATION
    # =====================================================

    category = models.CharField(
        max_length=40,
        choices=PropertyCategory.choices,
        db_index=True,
    )

    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.PROTECT,
        related_name="property_groups",
    )

    purpose = models.ForeignKey(
        PropertyPurpose,
        on_delete=models.PROTECT,
        related_name="property_groups",
    )

    # =====================================================
    # LOCATION
    # =====================================================

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="property_groups",
    )

    street_address = models.CharField(
        max_length=255,
        blank=True,
    )

    landmark = models.CharField(
        max_length=255,
        blank=True,
    )

    # =====================================================
    # PHYSICAL IDENTITY
    # =====================================================

    building_identifier = models.CharField(
        max_length=100,
        blank=True,
        help_text=(
            "Building, block, tower or structure identifier "
            "used when identifying the physical property."
        ),
    )

    unit_identifier = models.CharField(
        max_length=100,
        blank=True,
        help_text=(
            "Flat, apartment, room, shop, suite or unit identifier."
        ),
    )

    house_number = models.CharField(
        max_length=50,
        blank=True,
    )

    # =====================================================
    # PHYSICAL CHARACTERISTICS
    # =====================================================

    bedrooms = models.PositiveIntegerField(
        default=0,
    )

    bathrooms = models.PositiveIntegerField(
        default=0,
    )

    toilets = models.PositiveIntegerField(
        default=0,
    )

    parking_spaces = models.PositiveIntegerField(
        default=0,
    )

    floors = models.PositiveIntegerField(
        default=0,
    )

    units_available = models.PositiveIntegerField(
        default=1,
    )

    # =====================================================
    # SIZE
    # =====================================================

    class SizeUnit(models.TextChoices):
        SQUARE_METERS = (
            "sqm",
            "Square Metres",
        )
        SQUARE_FEET = (
            "sqft",
            "Square Feet",
        )
        ACRES = (
            "acres",
            "Acres",
        )
        HECTARES = (
            "hectares",
            "Hectares",
        )
        PLOTS = (
            "plots",
            "Plots",
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
    )

    building_size = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # =====================================================
    # PROPERTY DETAILS
    # =====================================================

    property_condition = models.ForeignKey(
        PropertyCondition,
        on_delete=models.PROTECT,
        related_name="property_groups",
        blank=True,
        null=True,
    )

    furnishing_status = models.ForeignKey(
        FurnishingStatus,
        on_delete=models.PROTECT,
        related_name="property_groups",
        blank=True,
        null=True,
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

    # =====================================================
    # AMENITIES
    # =====================================================

    amenities = models.ManyToManyField(
        Amenity,
        related_name="property_groups",
        blank=True,
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=[
                    "category",
                    "area",
                    "property_type",
                ],
                name="property_group_cat_area_idx",
            ),
            models.Index(
                fields=[
                    "area",
                    "property_type",
                    "purpose",
                    "bedrooms",
                ],
                name="property_group_id_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.property_type} - "
            f"{self.area}"
        )