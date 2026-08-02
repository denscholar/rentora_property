from rest_framework import serializers

from properties.models import (
    Amenity,
    AmenityCategory,
    FurnishingStatus,
    PropertyCondition,
    PropertyPurpose,
    PropertyType,
)


class PropertyTypeLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = (
            "uuid",
            "name",
            "code",
            "slug",
            "description",
            "icon",
        )


class PropertyPurposeLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPurpose
        fields = (
            "uuid",
            "name",
            "code",
            "slug",
            "description",
            "allow_viewing_booking",
        )


class PropertyConditionLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCondition
        fields = (
            "uuid",
            "name",
            "code",
            "slug",
            "description",
        )


class FurnishingStatusLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnishingStatus
        fields = (
            "uuid",
            "name",
            "code",
            "slug",
            "description",
        )


class AmenityCategoryLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityCategory
        fields = (
            "uuid",
            "name",
            "code",
            "slug",
            "description",
        )


class AmenityLookupSerializer(serializers.ModelSerializer):
    category = AmenityCategoryLookupSerializer(
        read_only=True,
    )

    class Meta:
        model = Amenity
        fields = (
            "uuid",
            "name",
            "slug",
            "description",
            "icon",
            "category",
        )