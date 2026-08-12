from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from core.api.responses import error_response, success_response
from locations.models import Area, Country, LGA, State
from locations.serializers import (
    AreaListSerializer,
    CountryListSerializer,
    LGAListSerializer,
    StateListSerializer,
)
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)


# =====================================================
# COUNTRY LIST
# =====================================================
class CountryListAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Locations"],
        summary="List active countries",
        description=(
            "Retrieve all active countries available for property "
            "location selection. Results are ordered by display order "
            "and country name."
        ),
        responses={
            200: CountryListSerializer(many=True),
        },
    )
    def get(self, request):
        countries = Country.objects.filter(
            is_active=True,
        ).order_by(
            "display_order",
            "name",
        )

        serializer = CountryListSerializer(
            countries,
            many=True,
        )

        return success_response(
            message="Countries retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# STATE LIST
# =====================================================
class StateListAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Locations"],
        summary="List states by country",
        description=(
            "Retrieve all active states belonging to a selected country. "
            "The country must be supplied as a UUID query parameter."
        ),
        parameters=[
            OpenApiParameter(
                name="uuid",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description=("UUID of the country whose states should be returned."),
            ),
        ],
        responses={
            200: StateListSerializer(many=True),
            400: OpenApiResponse(
                description="Country query parameter is required.",
            ),
            404: OpenApiResponse(
                description="Country was not found or is inactive.",
            ),
        },
    )
    def get(self, request):
        country_uuid = request.query_params.get("uuid")

        if not country_uuid:
            return error_response(
                message="Country is required.",
                errors={
                    "country": [
                        "Provide the country UUID.",
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        country = get_object_or_404(
            Country,
            uuid=country_uuid,
            is_active=True,
        )

        states = State.objects.filter(
            country=country,
            is_active=True,
        ).order_by(
            "display_order",
            "name",
        )

        serializer = StateListSerializer(
            states,
            many=True,
        )

        return success_response(
            message="States retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# LGA LIST
# =====================================================
class LGAListAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Locations"],
        summary="List LGAs by state",
        description=(
            "Retrieve all active Local Government Areas belonging to "
            "a selected state. The state must be supplied as an integer "
            "ID query parameter."
        ),
        parameters=[
            OpenApiParameter(
                name="uuid",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description=(
                    "Database UUID of the state whose LGAs should be returned."
                ),
            ),
        ],
        responses={
            200: LGAListSerializer(many=True),
            400: OpenApiResponse(
                description="State uuid query parameter is required.",
            ),
            404: OpenApiResponse(
                description="State uuid was not found or is inactive.",
            ),
        },
    )
    def get(self, request):
        state_uuid = request.query_params.get("uuid")

        if not state_uuid:
            return error_response(
                message="State is required.",
                errors={
                    "state": [
                        "Provide the state ID.",
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        state = get_object_or_404(
            State,
            uuid=state_uuid,
            is_active=True,
        )

        lgas = LGA.objects.filter(
            state=state,
            is_active=True,
        ).order_by(
            "display_order",
            "name",
        )

        serializer = LGAListSerializer(
            lgas,
            many=True,
        )

        return success_response(
            message="LGAs retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# AREA LIST
# =====================================================
class AreaListAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Locations"],
        summary="List areas by LGA",
        description=(
            "Retrieve all active areas or neighbourhoods belonging to "
            "a selected Local Government Area. The LGA must be supplied "
            "as a UUID query parameter."
        ),
        parameters=[
            OpenApiParameter(
                name="uuid",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description=("UUID of the LGA whose areas should be returned."),
            ),
        ],
        responses={
            200: AreaListSerializer(many=True),
            400: OpenApiResponse(
                description="LGA query parameter is required.",
            ),
            404: OpenApiResponse(
                description="LGA was not found or is inactive.",
            ),
        },
    )
    def get(self, request):
        lga_uuid = request.query_params.get("uuid")

        if not lga_uuid:
            return error_response(
                message="LGA is required.",
                errors={
                    "lga": [
                        "Provide the LGA UUID.",
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        lga = get_object_or_404(
            LGA,
            uuid=lga_uuid,
            is_active=True,
        )

        areas = Area.objects.filter(
            lga=lga,
            is_active=True,
        ).order_by(
            "display_order",
            "name",
        )

        serializer = AreaListSerializer(
            areas,
            many=True,
        )

        return success_response(
            message="Areas retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
