from core.api.responses import error_response, success_response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from property_verification.models.verification import PropertyVerification
from property_verification.services.property_verification_workflow import (
    PropertyVerificationWorkflow,
)


class SubmitPropertyVerificationForReviewAPIView(APIView):
    """
    Submits an authorized property verification
    for admin review.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Property Verification"],
        summary="Submit property verification for review",
        description=(
            "Moves an authorized property verification " "into the admin review queue."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description=(
                    "Property verification submitted " "for review successfully."
                ),
            ),
            400: OpenApiResponse(
                description="Invalid verification state.",
            ),
            404: OpenApiResponse(
                description="Property verification not found.",
            ),
        },
    )
    def post(self, request, uuid):
        try:
            verification = PropertyVerification.objects.select_related(
                "submission",
            ).get(
                uuid=uuid,
            )

        except PropertyVerification.DoesNotExist:
            return error_response(
                message="Property verification not found.",
                code="PROPERTY_VERIFICATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            PropertyVerificationWorkflow.submit_for_review(
                verification=verification,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_VERIFICATION_REVIEW_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message=(
                "Property verification submitted " "for admin review successfully."
            ),
            code="PROPERTY_VERIFICATION_SUBMITTED_FOR_REVIEW",
            data={
                "verification_uuid": str(verification.uuid),
                "status": verification.status,
            },
            status_code=status.HTTP_200_OK,
        )
