from rest_framework import serializers

from properties.api.serializers.submission.media import (
    PropertySubmissionMediaSerializer,
)
from properties.models.property.submission import PropertySubmission


class PropertySubmissionAdminDetailSerializer(
    serializers.ModelSerializer
):
    submitted_by = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    purpose = serializers.SerializerMethodField()
    property_condition = serializers.SerializerMethodField()
    furnishing_status = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    media = PropertySubmissionMediaSerializer(
        many=True,
        read_only=True,
    )
    reviewed_by = serializers.SerializerMethodField()

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    source_display = serializers.CharField(
        source="get_source_display",
        read_only=True,
    )

    class Meta:
        model = PropertySubmission

        fields = [
            "uuid",

            # Ownership / submission
            "submitted_by",
            "source",
            "source_display",

            # Moderation
            "status",
            "status_display",
            "reviewed_by",
            "reviewed_at",
            "review_note",

            # Classification
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",

            # Location
            "area",
            "street_address",
            "landmark",
            "latitude",
            "longitude",

            # Property information
            "title",
            "description",
            "bedrooms",
            "bathrooms",
            "toilets",
            "parking_spaces",
            "floors",
            "units_available",

            # Size
            "size_unit",
            "land_size",
            "building_size",

            # Rental information
            "payment_frequency",
            "proposed_price",
            "service_charge",
            "caution_fee",
            "legal_fee",
            "agency_fee",
            "is_negotiable",

            # Property condition
            "year_built",
            "is_new_build",
            "is_serviced",

            # Availability
            "available_from",
            "minimum_stay",

            # Amenities / media
            "amenities",
            "media",

            # Metadata
            "is_archived",
            "archived_at",
            "created_at",
            "updated_at",
        ]

    def get_submitted_by(self, obj):
        user = obj.submitted_by

        full_name_method = getattr(
            user,
            "get_full_name",
            None,
        )

        if callable(full_name_method):
            full_name = full_name_method()

            if full_name:
                return {
                    "uuid": str(user.slug),
                    "name": full_name,
                    "email": getattr(user, "email", ""),
                    "phone_number": getattr(
                        user,
                        "phone_number",
                        "",
                    ),
                }

        name = (
            f"{getattr(user, 'first_name', '')} "
            f"{getattr(user, 'last_name', '')}"
        ).strip()

        return {
            "uuid": str(user.uuid),
            "name": name or getattr(user, "email", ""),
            "email": getattr(user, "email", ""),
            "phone_number": getattr(
                user,
                "phone_number",
                "",
            ),
        }

    def get_property_type(self, obj):
        if not obj.property_type:
            return None

        return {
            "uuid": str(obj.property_type.uuid),
            "name": obj.property_type.name,
            "code": obj.property_type.code,
        }

    def get_purpose(self, obj):
        if not obj.purpose:
            return None

        return {
            "uuid": str(obj.purpose.uuid),
            "name": obj.purpose.name,
            "code": obj.purpose.code,
        }

    def get_property_condition(self, obj):
        if not obj.property_condition:
            return None

        return {
            "uuid": str(obj.property_condition.uuid),
            "name": obj.property_condition.name,
            "code": obj.property_condition.code,
        }

    def get_furnishing_status(self, obj):
        if not obj.furnishing_status:
            return None

        return {
            "uuid": str(obj.furnishing_status.uuid),
            "name": obj.furnishing_status.name,
            "code": obj.furnishing_status.code,
        }

    def get_area(self, obj):
        if not obj.area:
            return None

        area = obj.area

        return {
            "uuid": str(area.uuid),
            "name": area.name,
            "lga": (
                {
                    "uuid": str(area.lga.uuid),
                    "name": area.lga.name,
                }
                if area.lga
                else None
            ),
        }

    def get_amenities(self, obj):
        return [
            {
                "uuid": str(amenity.uuid),
                "name": amenity.name,
                "icon": amenity.icon,
            }
            for amenity in obj.amenities.all()
        ]

    def get_reviewed_by(self, obj):
        reviewer = obj.reviewed_by

        if reviewer is None:
            return None

        full_name_method = getattr(
            reviewer,
            "get_full_name",
            None,
        )

        if callable(full_name_method):
            full_name = full_name_method()

            if full_name:
                return {
                    "uuid": str(reviewer.slug),
                    "name": full_name,
                    "email": getattr(
                        reviewer,
                        "email",
                        "",
                    ),
                }

        name = (
            f"{getattr(reviewer, 'first_name', '')} "
            f"{getattr(reviewer, 'last_name', '')}"
        ).strip()

        return {
            "uuid": str(reviewer.uuid),
            "name": name or getattr(
                reviewer,
                "email",
                "",
            ),
            "email": getattr(
                reviewer,
                "email",
                "",
            ),
        }