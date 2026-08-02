from django.utils import timezone
from rest_framework import serializers
from decimal import Decimal

from locations.models import Area
from properties.models import (
    Amenity,
    FurnishingStatus,
    PropertyCondition,
    PropertyPurpose,
    PropertyType,
)


class PropertySubmissionInputSerializer(serializers.Serializer):
    """
    Validates data used to create or update a property-submission draft.

    The serializer validates API input only. It does not create or update
    PropertySubmission records directly.
    """

    property_type = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=PropertyType.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    purpose = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=PropertyPurpose.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    property_condition = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=PropertyCondition.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    furnishing_status = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=FurnishingStatus.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    area = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Area.objects.all(),
        required=False,
        allow_null=True,
    )

    amenities = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Amenity.objects.filter(is_active=True),
        many=True,
        required=False,
    )

    payment_frequency = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=20,
    )

    title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    landmark = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )

    street_address = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )

    bedrooms = serializers.IntegerField(
        required=False,
        min_value=0,
    )

    bathrooms = serializers.IntegerField(
        required=False,
        min_value=0,
    )

    toilets = serializers.IntegerField(
        required=False,
        min_value=0,
    )

    parking_spaces = serializers.IntegerField(
        required=False,
        min_value=0,
    )

    floors = serializers.IntegerField(
        required=False,
        min_value=0,
    )

    units_available = serializers.IntegerField(
        required=False,
        min_value=1,
    )

    year_built = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1800,
    )

    is_new_build = serializers.BooleanField(
        required=False,
    )

    is_serviced = serializers.BooleanField(
        required=False,
    )

    is_negotiable = serializers.BooleanField(
        required=False,
    )

    land_size = serializers.DecimalField(
        required=False,
        allow_null=True,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    building_size = serializers.DecimalField(
        required=False,
        allow_null=True,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    size_unit = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=30,
    )

    available_from = serializers.DateField(
        required=False,
        allow_null=True,
    )

    minimum_stay = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
    )

    proposed_price = serializers.DecimalField(
        required=False,
        allow_null=True,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    service_charge = serializers.DecimalField(
        required=False,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    caution_fee = serializers.DecimalField(
        required=False,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    legal_fee = serializers.DecimalField(
        required=False,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    agency_fee = serializers.DecimalField(
        required=False,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
    )

    latitude = serializers.DecimalField(
        required=False,
        allow_null=True,
        max_digits=10,
        decimal_places=7,
        min_value=Decimal("-90"),
        max_value=Decimal("90"),
    )

    longitude = serializers.DecimalField(
        required=False,
        allow_null=True,
        max_digits=10,
        decimal_places=7,
        min_value=Decimal("-180"),
        max_value=Decimal("180"),
    )

    def validate_year_built(self, value):
        if value is None:
            return value

        current_year = timezone.now().year

        if value > current_year:
            raise serializers.ValidationError(
                "Year built cannot be later than the current year."
            )

        return value

    def validate(self, attrs):
        land_size = attrs.get("land_size")
        building_size = attrs.get("building_size")
        size_unit = attrs.get("size_unit")

        if (land_size is not None or building_size is not None) and not size_unit:
            raise serializers.ValidationError(
                {
                    "size_unit": (
                        "Size unit is required when land size or "
                        "building size is provided."
                    )
                }
            )

        return attrs


class CreatePropertySubmissionSerializer(PropertySubmissionInputSerializer):
    """
    Input serializer for creating a new draft.
    """

    pass


class UpdatePropertySubmissionSerializer(PropertySubmissionInputSerializer):
    """
    Input serializer for partially updating a draft.
    """

    pass
