from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.api.responses import error_response, success_response

from properties.api.permissions import CanSubmitProperty
from properties.models import PropertySubmission
from properties.selectors import get_user_submission
from property_verification.api.serializers.initiation import (
    InitiatePropertyVerificationSerializer,
)
from property_verification.services.verification_email_service import (
    PropertyVerificationEmailService,
)
from property_verification.services.verification_service import (
    PropertyVerificationService,
)


class InitiatePropertyVerificationAPIView(APIView):
    """
    Allows an authorized property submitter to initiate
    verification for a property submission.
    """

    permission_classes = [
        IsAuthenticated,
        CanSubmitProperty,
    ]

    @extend_schema(
        tags=["Property Verification"],
        summary="Initiate property verification",
        description=(
            "Creates a property verification case and sends the "
            "landlord or authorized representative an invitation "
            "to verify the property."
        ),
        request=InitiatePropertyVerificationSerializer,
        responses={
            201: OpenApiResponse(
                description="Property verification initiated successfully.",
            ),
            400: OpenApiResponse(
                description="Invalid verification request.",
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
        # =========================================================
        # 1. Validate request data
        # =========================================================

        serializer = InitiatePropertyVerificationSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid property verification data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================================
        # 2. Find the user's submission
        # =========================================================

        try:
            submission = get_user_submission(
                user=request.user,
                uuid=submission_uuid,
            )

            if not PropertyVerificationService.can_initiate_verification(submission):
                return error_response(
                    message=(
                        "Property verification can only be requested "
                        "for properties that are under review or approved."
                    ),
                    code="PROPERTY_NOT_ELIGIBLE_FOR_VERIFICATION",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        except PropertySubmission.DoesNotExist:
            return error_response(
                message="Property submission not found.",
                code="PROPERTY_SUBMISSION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # =========================================================
        # 3. Initiate verification
        # =========================================================

        try:
            verification, token = PropertyVerificationService.initiate_verification(
                submission=submission,
                representative_name=serializer.validated_data["representative_name"],
                representative_email=serializer.validated_data["representative_email"],
                representative_role=serializer.validated_data["representative_role"],
                representative_phone=serializer.validated_data.get(
                    "representative_phone",
                    "",
                ),
                organization_name=serializer.validated_data.get(
                    "organization_name",
                    "",
                ),
            )

            # =========================================================
            # 4. Generate verification URL
            # =========================================================

            verification_url = PropertyVerificationService.build_verification_url(
                token,
            )

            PropertyVerificationEmailService.send_verification_invitation(
                verification=verification,
                verification_url=verification_url,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_VERIFICATION_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================================
        # 5. Return response
        # =========================================================

        return success_response(
            message=("Property verification initiated successfully."),
            code="PROPERTY_VERIFICATION_INITIATED",
            data={
                "verification_uuid": str(verification.uuid),
                "status": verification.status,
                "expires_at": verification.token_expires_at,
                "verification_url": verification_url,
            },
            status_code=status.HTTP_201_CREATED,
        )
