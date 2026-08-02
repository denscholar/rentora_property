from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.api.responses import success_response
from properties.models import (
    Amenity,
    AmenityCategory,
    FurnishingStatus,
    PropertyCondition,
    PropertyPurpose,
    PropertyType,
)
from properties.api.serializers.lookups import AmenityCategoryLookupSerializer, AmenityLookupSerializer, FurnishingStatusLookupSerializer, PropertyConditionLookupSerializer, PropertyPurposeLookupSerializer, PropertyTypeLookupSerializer



class BaseLookupAPIView(APIView):
    permission_classes = [AllowAny]

    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            is_active=True,
        ).order_by(
            "display_order",
            "name",
        )

    def get(self, request):
        self.request = request

        queryset = self.get_queryset()

        serializer = self.serializer_class(
            queryset,
            many=True,
        )

        return success_response(
            message="Lookup data retrieved successfully.",
            data=serializer.data,
        )


class PropertyTypeLookupAPIView(BaseLookupAPIView):
    model = PropertyType
    serializer_class = PropertyTypeLookupSerializer

    @extend_schema(
        tags=["Property Lookups"],
        summary="List property types",
        responses=PropertyTypeLookupSerializer(many=True),
    )
    def get(self, request):
        return super().get(request)


class PropertyPurposeLookupAPIView(BaseLookupAPIView):
    model = PropertyPurpose
    serializer_class = PropertyPurposeLookupSerializer

    @extend_schema(
        tags=["Property Lookups"],
        summary="List property purposes",
        responses=PropertyPurposeLookupSerializer(many=True),
    )
    def get(self, request):
        return super().get(request)


class PropertyConditionLookupAPIView(BaseLookupAPIView):
    model = PropertyCondition
    serializer_class = PropertyConditionLookupSerializer

    @extend_schema(
        tags=["Property Lookups"],
        summary="List property conditions",
        responses=PropertyConditionLookupSerializer(many=True),
    )
    def get(self, request):
        return super().get(request)


class FurnishingStatusLookupAPIView(BaseLookupAPIView):
    model = FurnishingStatus
    serializer_class = FurnishingStatusLookupSerializer

    @extend_schema(
        tags=["Property Lookups"],
        summary="List furnishing statuses",
        responses=FurnishingStatusLookupSerializer(many=True),
    )
    def get(self, request):
        return super().get(request)


class AmenityCategoryLookupAPIView(BaseLookupAPIView):
    model = AmenityCategory
    serializer_class = AmenityCategoryLookupSerializer

    @extend_schema(
        tags=["Property Lookups"],
        summary="List amenity categories",
        responses=AmenityCategoryLookupSerializer(many=True),
    )
    def get(self, request):
        return super().get(request)


class AmenityLookupAPIView(BaseLookupAPIView):
    model = Amenity
    serializer_class = AmenityLookupSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category")

        category_uuid = self.request.query_params.get("category")

        if category_uuid:
            queryset = queryset.filter(
                category__uuid=category_uuid,
            )

        return queryset

    @extend_schema(
        tags=["Property Lookups"],
        summary="List amenities",
        description=(
            "Returns active amenities. Optionally filter by " "amenity category UUID."
        ),
        responses=AmenityLookupSerializer(many=True),
    )
    def get(self, request):
        return super().get(request)
