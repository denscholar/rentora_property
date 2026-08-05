from rest_framework import serializers

from properties.models import PropertySubmission


class PropertySubmissionListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    property_type = serializers.CharField(
        source="property_type.name",
        read_only=True,
        allow_null=True,
    )

    purpose = serializers.CharField(
        source="purpose.name",
        read_only=True,
        allow_null=True,
    )

    area = serializers.CharField(
        source="area.name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = PropertySubmission
        fields = [
            "uuid",
            "title",
            "status",
            "status_display",
            "property_type",
            "purpose",
            "area",
            "bedrooms",
            "bathrooms",
            "proposed_price",
            "is_negotiable",
            "created_at",
            "updated_at",
        ]