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

from properties.api.serializers.eligibility import (
    PropertyEligibilityTestSerializer,
)

from properties.models import PropertySubmission

from properties.selectors.submission_selector import get_user_submission
from properties.services.eligibility_service import (
    PropertyEligibilityService,
)


class PropertyEligibilityConfigurationAPIView(APIView):
    """
    Create or update eligibility-test configuration
    for a property submission.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Property Eligibility"],
        summary="Configure property eligibility test",
        description=(
            "Creates or replaces the tenant eligibility "
            "test configuration for a property submission."
        ),
        request=PropertyEligibilityTestSerializer,
        responses={
            200: PropertyEligibilityTestSerializer,
            400: OpenApiResponse(
                description="Invalid eligibility configuration.",
            ),
            403: OpenApiResponse(
                description="You do not own this submission.",
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
        # =====================================================
        # 1. Validate payload
        # =====================================================

        serializer = PropertyEligibilityTestSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid eligibility test data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 2. Find authenticated user's submission
        # =====================================================

        try:
            submission = get_user_submission(
                user=request.user,
                uuid=submission_uuid,
            )

        except PropertySubmission.DoesNotExist:
            return error_response(
                message="Property submission not found.",
                code="PROPERTY_SUBMISSION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # =====================================================
        # 3. Configure
        # =====================================================

        try:
            eligibility_test = PropertyEligibilityService.configure_test(
                submission=submission,
                title=serializer.validated_data.get(
                    "title",
                    "Tenant Eligibility Test",
                ),
                description=serializer.validated_data.get(
                    "description",
                    "",
                ),
                is_active=serializer.validated_data.get(
                    "is_active",
                    True,
                ),
                questions=serializer.validated_data.get(
                    "questions",
                    [],
                ),
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_ELIGIBILITY_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 4. Mark submission as using eligibility test
        # =====================================================

        submission.is_eligibility_test = True

        submission.save(
            update_fields=[
                "is_eligibility_test",
                "updated_at",
            ]
        )

        # =====================================================
        # 5. Return
        # =====================================================

        output_serializer = PropertyEligibilityTestSerializer(
            eligibility_test,
        )

        return success_response(
            message=("Property eligibility test configured successfully."),
            code="PROPERTY_ELIGIBILITY_CONFIGURED",
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Property Eligibility"],
        summary="Get property eligibility test",
        responses={
            200: PropertyEligibilityTestSerializer,
            404: OpenApiResponse(
                description="Eligibility test not configured.",
            ),
        },
    )
    def get(
        self,
        request,
        submission_uuid,
    ):
        try:
            submission = get_user_submission(
                user=request.user,
                uuid=submission_uuid,
            )

        except PropertySubmission.DoesNotExist:
            return error_response(
                message="Property submission not found.",
                code="PROPERTY_SUBMISSION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        eligibility_test = getattr(
            submission,
            "eligibility_test",
            None,
        )

        if eligibility_test is None:
            return success_response(
                message="No eligibility test configured.",
                code="PROPERTY_ELIGIBILITY_NOT_CONFIGURED",
                data=None,
                status_code=status.HTTP_200_OK,
            )

        serializer = PropertyEligibilityTestSerializer(
            eligibility_test,
        )

        return success_response(
            message="Property eligibility test retrieved successfully.",
            code="PROPERTY_ELIGIBILITY_RETRIEVED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
