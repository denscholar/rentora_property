from rest_framework import serializers

from properties.models import PropertySubmission


class PublicPropertyListSerializer(serializers.ModelSerializer):
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

    cover_image = serializers.SerializerMethodField()

    verification = serializers.SerializerMethodField()

    class Meta:
        model = PropertySubmission
        fields = [
            "uuid",
            "title",
            "property_type",
            "purpose",
            "area",
            "bedrooms",
            "bathrooms",
            "toilets",
            "parking_spaces",
            "building_size",
            "land_size",
            "size_unit",
            "payment_frequency",
            "proposed_price",
            "service_charge",
            "caution_fee",
            "legal_fee",
            "agency_fee",
            "is_negotiable",
            "is_serviced",
            "is_new_build",
            "available_from",
            "verification",
            "cover_image",
        ]

    def get_cover_image(self, obj):
        media = (
            obj.media.filter(
                media_type="image",
                upload_status="completed",
            )
            .order_by(
                "-is_cover",
                "display_order",
                "created_at",
            )
            .first()
        )

        if media is None:
            return None

        return {
            "url": media.secure_url,
            "alt_text": media.alt_text or obj.title,
            "width": media.width,
            "height": media.height,
        }

    def get_verification(self, obj):
        return {
            "is_verified": True,
            "label": "SheltaMe Verified",
        }
