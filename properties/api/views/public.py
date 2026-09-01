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

# ==========================================
# LIST PROPERTIES FOR PUBLIC
# ==========================================


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
    success_response,
)

from properties.api.pagination import (
    PropertySubmissionPagination,
)

from properties.api.serializers.public.property_list import (
    PublicPropertyListSerializer,
)

from properties.selectors.public import (
    get_public_property_queryset,
)


class PublicPropertyListAPIView(APIView):
    """
    Returns properties that are publicly available
    on SheltaMe.
    """

    permission_classes = [
        AllowAny,
    ]

    pagination_class = PropertySubmissionPagination

    @extend_schema(
        tags=["Public Properties"],
        summary="List public properties",
        description=(
            "Returns only properties that are approved, " "verified and not archived."
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
                name="purpose",
                required=False,
                type=str,
                description="Filter by property purpose UUID.",
            ),
            OpenApiParameter(
                name="area",
                required=False,
                type=str,
                description="Filter by area UUID.",
            ),
            OpenApiParameter(
                name="bedrooms",
                required=False,
                type=int,
                description="Minimum number of bedrooms.",
            ),
            OpenApiParameter(
                name="min_price",
                required=False,
                type=float,
                description="Minimum property price.",
            ),
            OpenApiParameter(
                name="max_price",
                required=False,
                type=float,
                description="Maximum property price.",
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
        },
    )
    def get(self, request):
        queryset = get_public_property_queryset()

        # =====================================================
        # SEARCH
        # =====================================================

        search = request.query_params.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(area__name__icontains=search)
                | Q(property_type__name__icontains=search)
            )

        # =====================================================
        # FILTERS
        # =====================================================

        property_type = request.query_params.get("property_type", "").strip()

        purpose = request.query_params.get("purpose", "").strip()

        area = request.query_params.get("area", "").strip()

        bedrooms = request.query_params.get("bedrooms")

        min_price = request.query_params.get("min_price")

        max_price = request.query_params.get("max_price")

        if property_type:
            queryset = queryset.filter(
                property_type__uuid=property_type,
            )

        if purpose:
            queryset = queryset.filter(
                purpose__uuid=purpose,
            )

        if area:
            queryset = queryset.filter(
                area__uuid=area,
            )

        if bedrooms:
            queryset = queryset.filter(
                bedrooms__gte=bedrooms,
            )

        if min_price:
            queryset = queryset.filter(
                proposed_price__gte=min_price,
            )

        if max_price:
            queryset = queryset.filter(
                proposed_price__lte=max_price,
            )

        # =====================================================
        # PAGINATION
        # =====================================================

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


# ============================================
# DETAIL
# ===========================================
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
    def get(self, request, property_uuid):
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
