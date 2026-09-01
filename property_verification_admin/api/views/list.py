from drf_spectacular.utils import (
    OpenApiParameter,
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

from property_verification.models import PropertyVerification

from property_verification_admin.permissions import (
    CanReviewPropertyVerification,
)

from property_verification_admin.selectors import (
    get_admin_verification_queryset,
)

from property_verification_admin.serializers.list import (
    PropertyVerificationAdminListSerializer,
)


class PropertyVerificationAdminListAPIView(APIView):
    """
    Internal SheltaMe queue for property verification cases.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Verification Admin"],
        summary="List property verification cases",
        description=(
            "Returns property verification cases available to "
            "SheltaMe staff for internal review."
        ),
        parameters=[
            OpenApiParameter(
                name="status",
                required=False,
                type=str,
                enum=[
                    PropertyVerification.VerificationStatus.PENDING,
                    PropertyVerification.VerificationStatus.AUTHORIZATION_SENT,
                    PropertyVerification.VerificationStatus.AUTHORIZED,
                    PropertyVerification.VerificationStatus.UNDER_REVIEW,
                    PropertyVerification.VerificationStatus.VERIFIED,
                    PropertyVerification.VerificationStatus.REJECTED,
                    PropertyVerification.VerificationStatus.EXPIRED,
                    PropertyVerification.VerificationStatus.CANCELLED,
                ],
                description="Filter verification cases by status.",
            ),
        ],
        responses={
            200: PropertyVerificationAdminListSerializer(
                many=True,
            ),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            403: OpenApiResponse(
                description="Verification review permission required.",
            ),
        },
    )
    def get(self, request):
        queryset = get_admin_verification_queryset()

        requested_status = request.query_params.get(
            "status",
            PropertyVerification.VerificationStatus.UNDER_REVIEW,
        )

        if requested_status:
            valid_statuses = {
                value for value, _ in (PropertyVerification.VerificationStatus.choices)
            }

            if requested_status not in valid_statuses:
                return error_response(
                    message="Invalid verification status.",
                    errors={"status": ["Invalid verification status."]},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            queryset = queryset.filter(
                status=requested_status,
            )

        serializer = PropertyVerificationAdminListSerializer(
            queryset,
            many=True,
        )

        return success_response(
            message=("Property verification cases retrieved successfully."),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
