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


from properties.models.property.eligibility import PropertyEligibilityAttempt
from properties.selectors.public import (
    get_public_property_queryset,
)

from properties.api.serializers.eligibility_attempt import (
    PropertyEligibilityAttemptSerializer,
)


class StartPropertyEligibilityAPIView(APIView):
    """
    Starts an eligibility test for a publicly listed property.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Property Eligibility"],
        summary="Start property eligibility test",
        responses={
            201: PropertyEligibilityAttemptSerializer,
            400: OpenApiResponse(
                description="Eligibility test cannot be started.",
            ),
            404: OpenApiResponse(
                description="Public property not found.",
            ),
        },
    )
    def post(
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

        if not property_submission.is_eligibility_test:
            return error_response(
                message=("This property does not require " "an eligibility test."),
                code="ELIGIBILITY_TEST_NOT_REQUIRED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        eligibility_test = getattr(
            property_submission,
            "eligibility_test",
            None,
        )

        if eligibility_test is None or not eligibility_test.is_active:
            return error_response(
                message=(
                    "This property's eligibility test " "is currently unavailable."
                ),
                code="ELIGIBILITY_TEST_UNAVAILABLE",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        attempt = PropertyEligibilityAttempt.objects.create(
            test=eligibility_test,
            tenant=request.user,
        )

        serializer = PropertyEligibilityAttemptSerializer(
            attempt,
        )

        return success_response(
            message=("Property eligibility test started successfully."),
            code="ELIGIBILITY_ATTEMPT_STARTED",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )
