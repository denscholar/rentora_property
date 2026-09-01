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
    get_admin_submission_queryset,
)
from property_verification_admin.serializers.submission_detail import PropertySubmissionAdminDetailSerializer



class PropertySubmissionAdminDetailAPIView(APIView):
    """
    Returns the full property submission for internal
    SheltaMe moderation.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Submission Admin"],
        summary="Retrieve property submission for moderation",
        description=(
            "Returns the complete property submission so a "
            "SheltaMe reviewer can assess it before approval "
            "or rejection."
        ),
        responses={
            200: PropertySubmissionAdminDetailSerializer,
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            403: OpenApiResponse(
                description="Moderation permission required.",
            ),
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def get(
        self,
        request,
        submission_uuid,
    ):
        submission = (
            get_admin_submission_queryset()
            .filter(
                uuid=submission_uuid,
            )
            .first()
        )

        if submission is None:
            return error_response(
                message="Property submission not found.",
                code="PROPERTY_SUBMISSION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = PropertySubmissionAdminDetailSerializer(
            submission,
            context={
                "request": request,
            },
        )

        return success_response(
            message=("Property submission retrieved successfully."),
            code="PROPERTY_SUBMISSION_RETRIEVED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
