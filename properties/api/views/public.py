from django.db.models import Q

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.api.responses import (
    error_response,
    success_response,
)

from properties.api.pagination import PropertySubmissionPagination
from properties.api.serializers.public.property_detail import (
    PublicPropertyDetailSerializer,
)
from properties.api.serializers.public.property_list import (
    PublicPropertyListSerializer,
)
from properties.selectors.public import (
    get_public_property_queryset,
)

# ============================================================
# PUBLIC PROPERTY LIST
# ============================================================


class PublicPropertyListAPIView(APIView):
    """
    Returns properties that are publicly available on SheltaMe.

    Public visibility is determined entirely by the public selector.
    This view is responsible only for:
        - search
        - filtering
        - sorting
        - pagination
    """

    permission_classes = [
        AllowAny,
    ]

    pagination_class = PropertySubmissionPagination

    # ========================================================
    # PRICE RANGE CONTRACT
    # ========================================================

    PRICE_RANGES = {
        "under_1m": {
            "max_exclusive": 1_000_000,
        },
        "1m_3m": {
            "min": 1_000_000,
            "max_exclusive": 3_000_000,
        },
        "3m_5m": {
            "min": 3_000_000,
            "max_exclusive": 5_000_000,
        },
        "5m_10m": {
            "min": 5_000_000,
            "max_exclusive": 10_000_000,
        },
        "10m_plus": {
            "min": 10_000_000,
        },
    }

    # ========================================================
    # SORTING CONTRACT
    # ========================================================

    ALLOWED_ORDERING = {
        "-created_at": "-created_at",
        "proposed_price": "proposed_price",
        "-proposed_price": "-proposed_price",
    }

    # ========================================================
    # SCHEMA
    # ========================================================

    @extend_schema(
        tags=["Public Properties"],
        summary="List public properties",
        description=(
            "Returns only properties that are approved, verified " "and not archived."
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                required=False,
                type=str,
                description=(
                    "Search property title, description, " "area or property type."
                ),
            ),
            OpenApiParameter(
                name="property_type",
                required=False,
                type=str,
                description="Filter by property type UUID.",
            ),
            OpenApiParameter(
                name="price_range",
                required=False,
                type=str,
                enum=[
                    "under_1m",
                    "1m_3m",
                    "3m_5m",
                    "5m_10m",
                    "10m_plus",
                ],
                description=("Filter by predefined property price range."),
            ),
            OpenApiParameter(
                name="ordering",
                required=False,
                type=str,
                enum=[
                    "-created_at",
                    "proposed_price",
                    "-proposed_price",
                ],
                description=("Sort properties. " "Default: newest first."),
            ),
            OpenApiParameter(
                name="page",
                required=False,
                type=int,
                description="Page number.",
            ),
            OpenApiParameter(
                name="page_size",
                required=False,
                type=int,
                description=("Number of properties per page. " "Maximum 50."),
            ),
        ],
        responses={
            200: PublicPropertyListSerializer(
                many=True,
            ),
            400: OpenApiResponse(
                description="Invalid query parameter.",
            ),
        },
    )
    def get(self, request):
        # ====================================================
        # BASE PUBLIC QUERYSET
        # ====================================================

        queryset = get_public_property_queryset()

        # ====================================================
        # SEARCH
        # ====================================================

        search = request.query_params.get(
            "search",
            "",
        ).strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(area__name__icontains=search)
                | Q(property_type__name__icontains=search)
            )

        # ====================================================
        # PROPERTY TYPE
        # ====================================================

        property_type = request.query_params.get(
            "property_type",
            "",
        ).strip()

        if property_type:
            queryset = queryset.filter(
                property_type__uuid=property_type,
            )

        # ====================================================
        # PRICE RANGE
        # ====================================================

        price_range = (
            request.query_params.get(
                "price_range",
                "",
            )
            .strip()
            .lower()
        )

        if price_range:
            price_config = self.PRICE_RANGES.get(
                price_range,
            )

            if price_config is None:
                return error_response(
                    message="Invalid price range.",
                    code="INVALID_PRICE_RANGE",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            min_price = price_config.get("min")
            max_exclusive = price_config.get(
                "max_exclusive",
            )

            if min_price is not None:
                queryset = queryset.filter(
                    proposed_price__gte=min_price,
                )

            if max_exclusive is not None:
                queryset = queryset.filter(
                    proposed_price__lt=max_exclusive,
                )

        # ====================================================
        # SORTING
        # ====================================================

        requested_ordering = request.query_params.get(
            "ordering",
            "-created_at",
        ).strip()

        ordering = self.ALLOWED_ORDERING.get(
            requested_ordering,
            "-created_at",
        )

        queryset = queryset.order_by(
            ordering,
        )

        # ====================================================
        # PAGINATION
        # ====================================================

        paginator = self.pagination_class()

        page = paginator.paginate_queryset(
            queryset,
            request,
            view=self,
        )

        serializer = PublicPropertyListSerializer(
            page,
            many=True,
            context={
                "request": request,
            },
        )

        paginated_data = paginator.get_paginated_data(
            serializer.data,
        )

        return success_response(
            message="Public properties retrieved successfully.",
            code="PUBLIC_PROPERTIES_RETRIEVED",
            data=paginated_data,
            status_code=status.HTTP_200_OK,
        )


# ============================================================
# PUBLIC PROPERTY DETAIL
# ============================================================


class PublicPropertyDetailAPIView(APIView):
    """
    Returns a single publicly listable property.
    """

    permission_classes = [
        AllowAny,
    ]

    @extend_schema(
        tags=["Public Properties"],
        summary="Retrieve public property",
        description=(
            "Returns a single property only when it is "
            "approved, verified and not archived."
        ),
        responses={
            200: PublicPropertyDetailSerializer,
            404: OpenApiResponse(
                description="Public property not found.",
            ),
        },
    )
    def get(
        self,
        request,
        property_uuid,
    ):
        property_submission = (
            get_public_property_queryset()
            .filter(
                uuid=property_uuid,
            )
            .first()
        )

        if property_submission is None:
            return error_response(
                message="Property not found.",
                code="PUBLIC_PROPERTY_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = PublicPropertyDetailSerializer(
            property_submission,
            context={
                "request": request,
            },
        )

        return success_response(
            message="Public property retrieved successfully.",
            code="PUBLIC_PROPERTY_RETRIEVED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
