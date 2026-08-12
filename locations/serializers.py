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
    class Meta:
        model = State
        fields = [
            "uuid",
            "name",
            "is_active",
            "slug",
        ]


class LGAListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LGA
        fields = [
            "uuid",
            "name",
            "slug",
            "is_active",
        ]


class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "uuid",
            "name",
            "slug",
            "latitude",
            "longitude",
        ]
