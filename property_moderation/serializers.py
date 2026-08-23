from rest_framework import serializers

from properties.models import PropertySubmission
from properties.models.lookups.amenity import Amenity


class PropertyModerationAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "id",
            "name",
        ]


class PropertyModerationSubmissionListSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.SerializerMethodField()
    submitted_by_email = serializers.EmailField(
        source="submitted_by.email",
        read_only=True,
    )

    property_type_name = serializers.CharField(
        source="property_type.name",
        read_only=True,
    )

    purpose_name = serializers.CharField(
        source="purpose.name",
        read_only=True,
    )

    area_name = serializers.CharField(
        source="area.name",
        read_only=True,
    )
    amenities = PropertyModerationAmenitySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = PropertySubmission
        fields = [
            "id",
            "title",
            "status",
            "amenities",
            "source",
            "submitted_by",
            "submitted_by_name",
            "submitted_by_email",
            "property_type",
            "property_type_name",
            "purpose",
            "purpose_name",
            "area",
            "area_name",
            "proposed_price",
            "payment_frequency",
            "created_at",
        ]
        read_only_fields = fields

    def get_submitted_by_name(self, obj):
        return obj.submitted_by.get_full_name()


class PropertyModerationSubmissionDetailSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.SerializerMethodField()
    submitted_by_email = serializers.EmailField(
        source="submitted_by.email",
        read_only=True,
    )

    property_type_name = serializers.CharField(
        source="property_type.name",
        read_only=True,
    )

    purpose_name = serializers.CharField(
        source="purpose.name",
        read_only=True,
    )

    property_condition_name = serializers.CharField(
        source="property_condition.name",
        read_only=True,
    )

    furnishing_status_name = serializers.CharField(
        source="furnishing_status.name",
        read_only=True,
    )

    area_name = serializers.CharField(
        source="area.name",
        read_only=True,
    )

    submitted_property_group_id = serializers.UUIDField(
        source="property_group.id",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = PropertySubmission

        fields = [
            # =================================================
            # ID / WORKFLOW
            # =================================================
            "id",
            "status",
            "source",
            # =================================================
            # SUBMITTER
            # =================================================
            "submitted_by",
            "submitted_by_name",
            "submitted_by_email",
            # =================================================
            # PROPERTY CLASSIFICATION
            # =================================================
            "property_type",
            "property_type_name",
            "purpose",
            "purpose_name",
            "property_condition",
            "property_condition_name",
            "furnishing_status",
            "furnishing_status_name",
            # =================================================
            # LOCATION
            # =================================================
            "area",
            "area_name",
            "street_address",
            "landmark",
            # =================================================
            # PROPERTY DETAILS
            # =================================================
            "title",
            "description",
            "bedrooms",
            "bathrooms",
            "toilets",
            "parking_spaces",
            "floors",
            "units_available",
            # =================================================
            # SIZE
            # =================================================
            "size_unit",
            "land_size",
            "building_size",
            # =================================================
            # PROPERTY CHARACTERISTICS
            # =================================================
            "year_built",
            "is_new_build",
            "is_serviced",
            # =================================================
            # AMENITIES
            # =================================================
            "amenities",
            # =================================================
            # PRICING
            # =================================================
            "proposed_price",
            "payment_frequency",
            "service_charge",
            "caution_fee",
            "legal_fee",
            "agency_fee",
            "is_negotiable",
            # =================================================
            # AVAILABILITY
            # =================================================
            "available_from",
            "minimum_stay",
            # =================================================
            # DUPLICATE / MODERATION
            # =================================================
            "property_group",
            "submitted_property_group_id",
            "duplicate_similarity_score",
            "review_note",
            "reviewed_by",
            "reviewed_at",
            # =================================================
            # META
            # =================================================
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields

    def get_submitted_by_name(self, obj):
        return obj.submitted_by.get_full_name()
