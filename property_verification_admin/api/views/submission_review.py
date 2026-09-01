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

from property_verification_admin.serializers.submission_review import (
    PropertySubmissionReviewSerializer,
)
from property_verification_admin.services import PropertySubmissionModerationService

# ===============================================
# PROPERTY ADMIN APPROVE
# =================================================


class PropertySubmissionAdminApproveAPIView(APIView):
    """
    Approves a property submission after internal moderation.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Submission Admin"],
        summary="Approve property submission",
        description=("Approves a property submission currently under " "review."),
        request=PropertySubmissionReviewSerializer,
        responses={
            200: OpenApiResponse(
                description="Property submission approved.",
            ),
            400: OpenApiResponse(
                description="Submission cannot be approved.",
            ),
            403: OpenApiResponse(
                description="Moderation permission required.",
            ),
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def post(
        self,
        request,
        submission_uuid,
    ):
        serializer = PropertySubmissionReviewSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid moderation data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

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

        try:
            submission = PropertySubmissionModerationService.approve(
                submission=submission,
                reviewer=request.user,
                review_note=serializer.validated_data.get(
                    "review_note",
                    "",
                ),
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_SUBMISSION_APPROVAL_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Property submission approved successfully.",
            code="PROPERTY_SUBMISSION_APPROVED",
            data={
                "submission_uuid": str(submission.uuid),
                "status": submission.status,
                "reviewed_at": submission.reviewed_at,
                "reviewed_by": str(request.user.slug),
                "review_note": submission.review_note,
            },
            status_code=status.HTTP_200_OK,
        )


# ===============================================
# PROPERTY ADMIN REJECT
# =================================================


class PropertySubmissionAdminRejectAPIView(APIView):
    """
    Rejects a property submission after internal moderation.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Submission Admin"],
        summary="Reject property submission",
        description=(
            "Rejects a property submission currently under "
            "review. A rejection reason is required."
        ),
        request=PropertySubmissionReviewSerializer,
        responses={
            200: OpenApiResponse(
                description="Property submission rejected.",
            ),
            400: OpenApiResponse(
                description="Submission cannot be rejected.",
            ),
            403: OpenApiResponse(
                description="Moderation permission required.",
            ),
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def post(
        self,
        request,
        submission_uuid,
    ):
        serializer = PropertySubmissionReviewSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid moderation data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        review_note = serializer.validated_data.get("review_note", "").strip()

        if not review_note:
            return error_response(
                message="A rejection reason is required.",
                errors={
                    "review_note": [
                        "Please provide a reason for rejecting this property submission."
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

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

        try:
            submission = PropertySubmissionModerationService.reject(
                submission=submission,
                reviewer=request.user,
                review_note=review_note,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_SUBMISSION_REJECTION_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Property submission rejected successfully.",
            code="PROPERTY_SUBMISSION_REJECTED",
            data={
                "submission_uuid": str(submission.uuid),
                "status": submission.status,
                "reviewed_at": submission.reviewed_at,
                "reviewed_by": str(request.user.uuid),
                "review_note": submission.review_note,
            },
            status_code=status.HTTP_200_OK,
        )
