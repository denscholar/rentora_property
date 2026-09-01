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

from property_verification.models import PropertyVerification

from property_verification_admin.permissions import (
    CanReviewPropertyVerification,
)

from property_verification_admin.serializers.review import (
    PropertyVerificationReviewSerializer,
)
from property_verification_admin.services import PropertySubmissionModerationService, PropertyVerificationAdminService

# from property_verification_admin.services import (
#     PropertyVerificationAdminService,
# )

# =======================================================
# VERIFY/APPROVE API VIEW
# =======================================================


class PropertyVerificationAdminVerifyAPIView(APIView):
    """
    Allows authorized SheltaMe staff to verify a property.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Verification Admin"],
        summary="Verify property verification",
        description=(
            "Marks an UNDER_REVIEW property verification as "
            "VERIFIED. The related property submission must "
            "already be APPROVED."
        ),
        request=PropertyVerificationReviewSerializer,
        responses={
            200: OpenApiResponse(
                description="Property verification approved.",
            ),
            400: OpenApiResponse(
                description="Verification cannot be approved.",
            ),
            403: OpenApiResponse(
                description="Verification review permission required.",
            ),
            404: OpenApiResponse(
                description="Verification case not found.",
            ),
        },
    )
    def post(
        self,
        request,
        uuid,
    ):
        # =====================================================
        # 1. Validate request
        # =====================================================

        serializer = PropertyVerificationReviewSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid review data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 2. Find verification
        # =====================================================

        verification = (
            PropertyVerification.objects.select_related(
                "submission",
            )
            .filter(
                uuid=uuid,
            )
            .first()
        )

        if verification is None:
            return error_response(
                message="Property verification not found.",
                code="PROPERTY_VERIFICATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # =====================================================
        # 3. Perform verification
        # =====================================================

        try:
            verification = PropertyVerificationAdminService.verify(
                verification=verification,
                reviewer=request.user,
                review_note=serializer.validated_data.get(
                    "review_note",
                    "",
                ),
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_VERIFICATION_VERIFY_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 4. Return result
        # =====================================================

        return success_response(
            message=("Property verification approved successfully."),
            code="PROPERTY_VERIFICATION_VERIFIED",
            data={
                "verification_uuid": str(verification.uuid),
                "status": verification.status,
                "verified_at": verification.verified_at,
                "reviewed_by": str(request.user.slug),
            },
            status_code=status.HTTP_200_OK,
        )


# =================================================
# REJECT API VIEW
# =================================================


class PropertyVerificationAdminRejectAPIView(APIView):
    """
    Allows authorized SheltaMe staff to reject a property
    verification.
    """

    permission_classes = [
        IsAuthenticated,
        CanReviewPropertyVerification,
    ]

    @extend_schema(
        tags=["Property Verification Admin"],
        summary="Reject property verification",
        description=(
            "Rejects an UNDER_REVIEW property verification. "
            "A rejection reason is required."
        ),
        request=PropertyVerificationReviewSerializer,
        responses={
            200: OpenApiResponse(
                description="Property verification rejected.",
            ),
            400: OpenApiResponse(
                description="Verification cannot be rejected.",
            ),
            403: OpenApiResponse(
                description="Verification review permission required.",
            ),
            404: OpenApiResponse(
                description="Verification case not found.",
            ),
        },
    )
    def post(
        self,
        request,
        uuid,
    ):
        # =====================================================
        # 1. Validate request
        # =====================================================

        serializer = PropertyVerificationReviewSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid review data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 2. Require rejection reason
        # =====================================================

        review_note = serializer.validated_data.get("review_note", "").strip()

        if not review_note:
            return error_response(
                message="A rejection reason is required.",
                errors={
                    "review_note": [
                        "Please provide a reason for rejecting this verification."
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 3. Find verification
        # =====================================================

        verification = (
            PropertyVerification.objects.select_related(
                "submission",
            )
            .filter(
                uuid=uuid,
            )
            .first()
        )

        if verification is None:
            return error_response(
                message="Property verification not found.",
                code="PROPERTY_VERIFICATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # =====================================================
        # 4. Perform rejection
        # =====================================================

        try:
            verification = PropertyVerificationAdminService.reject(
                verification=verification,
                reviewer=request.user,
                review_note=review_note,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_VERIFICATION_REJECT_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 5. Return result
        # =====================================================

        return success_response(
            message=("Property verification rejected successfully."),
            code="PROPERTY_VERIFICATION_REJECTED",
            data={
                "verification_uuid": str(verification.uuid),
                "status": verification.status,
                "rejected_at": verification.rejected_at,
                "reviewed_by": str(request.user.slug),
                "review_note": verification.review_note,
            },
            status_code=status.HTTP_200_OK,
        )
