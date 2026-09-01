from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.api.responses import (
    error_response,
    success_response,
)

from property_verification_admin.permissions import (
    CanReviewPropertyVerification,
)

from property_verification_admin.selectors import (
    get_admin_verification_detail_queryset,
)
from property_verification_admin.serializers.detail import PropertyVerificationAdminDetailSerializer




class PropertyVerificationAdminDetailAPIView(APIView):
    """
    Returns the complete details of one property verification
    case for internal SheltaMe review.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Verification Admin"],
        summary="Retrieve verification case",
        description=(
            "Returns the complete property verification case, "
            "including the property, agent, representative, "
            "authorization response and submitted documents."
        ),
        responses={
            200: PropertyVerificationAdminDetailSerializer,
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            403: OpenApiResponse(
                description=("Verification review permission required."),
            ),
            404: OpenApiResponse(
                description="Verification case not found.",
            ),
        },
    )
    def get(self, request, uuid):
        queryset = get_admin_verification_detail_queryset()

        verification = queryset.filter(
            uuid=uuid,
        ).first()

        if verification is None:
            return error_response(
                message="Property verification not found.",
                code="PROPERTY_VERIFICATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = PropertyVerificationAdminDetailSerializer(
            verification,
            context={
                "request": request,
            },
        )

        return success_response(
            message=("Property verification retrieved successfully."),
            code="PROPERTY_VERIFICATION_RETRIEVED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
