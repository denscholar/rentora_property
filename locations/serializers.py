from rest_framework import serializers

from locations.models import Area, Country, LGA, State


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "uuid",
            "name",
            "code",
            "slug",
        ]


class StateListSerializer(serializers.ModelSerializer):
    country_uuid = serializers.UUIDField(
        source="country.uuid",
        read_only=True,
    )

    class Meta:
        model = State
        fields = [
            "id",
            "name",
            "slug",
            "country_uuid",
        ]


class LGAListSerializer(serializers.ModelSerializer):
    state_id = serializers.IntegerField(
        source="state.id",
        read_only=True,
    )

    class Meta:
        model = LGA
        fields = [
            "uuid",
            "name",
            "slug",
            "state_id",
        ]


class AreaListSerializer(serializers.ModelSerializer):
    lga_uuid = serializers.UUIDField(
        source="lga.uuid",
        read_only=True,
    )

    class Meta:
        model = Area
        fields = [
            "uuid",
            "name",
            "slug",
            "latitude",
            "longitude",
            "lga_uuid",
        ]
