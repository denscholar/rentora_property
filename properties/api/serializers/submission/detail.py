from rest_framework import serializers

from locations.models import Area
from properties.models import (
    Amenity,
    FurnishingStatus,
    PropertyCondition,
    PropertyPurpose,
    PropertySubmission,
    PropertyType,
)


class PropertyTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = [
            "uuid",
            "name",
            "code",
            "icon",
        ]


class PropertyPurposeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPurpose
        fields = [
            "uuid",
            "name",
            "code",
            "allow_viewing_booking",
        ]


class PropertyConditionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCondition
        fields = [
            "uuid",
            "name",
            "code",
        ]


class FurnishingStatusSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnishingStatus
        fields = [
            "uuid",
            "name",
            "code",
        ]


class AmenitySummarySerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Amenity
        fields = [
            "uuid",
            "name",
            "icon",
            "category",
        ]


class AreaSummarySerializer(serializers.ModelSerializer):
    lga = serializers.CharField(
        source="lga.name",
        read_only=True,
    )

    state = serializers.CharField(
        source="lga.state.name",
        read_only=True,
    )

    country = serializers.CharField(
        source="lga.state.country.name",
        read_only=True,
    )

    class Meta:
        model = Area
        fields = [
            "uuid",
            "name",
            "lga",
            "state",
            "country",
        ]


class PropertySubmissionDetailSerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSummarySerializer(
        read_only=True,
    )

    purpose = PropertyPurposeSummarySerializer(
        read_only=True,
    )

    property_condition = PropertyConditionSummarySerializer(
        read_only=True,
    )

    furnishing_status = FurnishingStatusSummarySerializer(
        read_only=True,
    )

    area = AreaSummarySerializer(
        read_only=True,
    )

    amenities = AmenitySummarySerializer(
        many=True,
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    source_display = serializers.CharField(
        source="get_source_display",
        read_only=True,
    )

    submitted_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PropertySubmission
        fields = [
            "uuid",
            "submitted_by_name",
            "source",
            "source_display",
            "status",
            "status_display",
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
            "area",
            "amenities",
            "payment_frequency",
            "title",
            "description",
            "landmark",
            "street_address",
            "bedrooms",
            "bathrooms",
            "toilets",
            "parking_spaces",
            "floors",
            "units_available",
            "year_built",
            "is_new_build",
            "is_serviced",
            "is_negotiable",
            "land_size",
            "building_size",
            "size_unit",
            "available_from",
            "minimum_stay",
            "proposed_price",
            "service_charge",
            "caution_fee",
            "legal_fee",
            "agency_fee",
            "latitude",
            "longitude",
            "duplicate_similarity_score",
            "review_note",
            "reviewed_at",
            "is_archived",
            "archived_at",
            "created_at",
            "updated_at",
        ]

    def get_submitted_by_name(self, obj):
        user = obj.submitted_by

        full_name_method = getattr(user, "get_full_name", None)

        if callable(full_name_method):
            full_name = full_name_method()

            if full_name:
                return full_name

        first_name = getattr(user, "first_name", "")
        last_name = getattr(user, "last_name", "")

        full_name = f"{first_name} {last_name}".strip()

        return full_name or getattr(user, "email", "")
