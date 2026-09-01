from rest_framework import serializers

from properties.api.serializers.public.property_list import (
    PublicPropertyListSerializer,
)
from properties.models import PropertySubmission


class PublicPropertyDetailSerializer(PublicPropertyListSerializer):
    media = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    description = serializers.CharField(
        read_only=True,
    )

    class Meta(PublicPropertyListSerializer.Meta):
        fields = PublicPropertyListSerializer.Meta.fields + [
            "description",
            "year_built",
            "floors",
            "units_available",
            "media",
            "amenities",
        ]

    def get_media(self, obj):
        media_queryset = obj.media.filter(
            upload_status="completed",
        ).order_by(
            "display_order",
            "created_at",
        )

        return [
            {
                "uuid": str(media.uuid),
                "media_type": media.media_type,
                "url": media.secure_url,
                "alt_text": media.alt_text or obj.title,
                "caption": media.caption,
                "display_order": media.display_order,
                "is_cover": media.is_cover,
                "width": media.width,
                "height": media.height,
                "duration": media.duration,
            }
            for media in media_queryset
        ]

    def get_amenities(self, obj):
        return [
            {
                "uuid": str(amenity.uuid),
                "name": amenity.name,
                "icon": amenity.icon,
            }
            for amenity in obj.amenities.all()
        ]
