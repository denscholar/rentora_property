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


from properties.models.property.eligibility import PropertyEligibilityAnswer, PropertyEligibilityAttempt
from properties.selectors.public import (
    get_public_property_queryset,
)

from properties.api.serializers.eligibility_attempt import (
    PropertyEligibilityAttemptSerializer,
    SubmitEligibilityAttemptSerializer,
)
from properties.services.eligibility_evaluation import PropertyEligibilityEvaluationService


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

# ======================================================
# SUBMIT AND EVALUATE TENANT ELIGIBILITY TEST 
# ======================================================
class SubmitPropertyEligibilityAPIView(APIView):
    """
    Submit and evaluate a tenant's eligibility test.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Property Eligibility"],
        summary="Submit property eligibility test",
        request=SubmitEligibilityAttemptSerializer,
        responses={
            200: OpenApiResponse(
                description="Eligibility test evaluated.",
            ),
            400: OpenApiResponse(
                description="Invalid eligibility answers.",
            ),
            404: OpenApiResponse(
                description="Eligibility attempt not found.",
            ),
        },
    )
    def post(
        self,
        request,
        attempt_uuid,
    ):
        attempt = (
            PropertyEligibilityAttempt.objects
            .select_related(
                "test",
                "test__submission",
            )
            .prefetch_related(
                "test__questions__options",
                "test__questions__rule",
                "answers",
            )
            .filter(
                uuid=attempt_uuid,
                tenant=request.user,
            )
            .first()
        )

        if attempt is None:
            return error_response(
                message="Eligibility attempt not found.",
                code="ELIGIBILITY_ATTEMPT_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = SubmitEligibilityAttemptSerializer(
            data=request.data,
            context={
                "attempt": attempt,
            },
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid eligibility answers.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            for answer_data in serializer.validated_data["answers"]:
                question_uuid = answer_data["question"]

                question = (
                    attempt.test.questions
                    .filter(
                        uuid=question_uuid,
                        is_active=True,
                    )
                    .first()
                )

                if question is None:
                    raise ValueError(
                        "One or more submitted questions are invalid."
                    )

                PropertyEligibilityAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={
                        "answer_text": answer_data.get(
                            "answer_text",
                            "",
                        ),
                        "selected_options": answer_data.get(
                            "selected_options",
                            [],
                        ),
                        "answer_number": answer_data.get(
                            "answer_number",
                        ),
                        "answer_date": answer_data.get(
                            "answer_date",
                        ),
                    },
                )

            result = (
                PropertyEligibilityEvaluationService.evaluate(
                    attempt=attempt,
                )
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                code="ELIGIBILITY_EVALUATION_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message=(
                "Property eligibility test evaluated successfully."
            ),
            code="ELIGIBILITY_TEST_EVALUATED",
            data={
                "attempt_uuid": str(attempt.uuid),
                "passed": result["passed"],
                "results": result["results"],
            },
            status_code=status.HTTP_200_OK,
        )