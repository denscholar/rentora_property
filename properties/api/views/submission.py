from django.core.exceptions import ValidationError as DjangoValidationError

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
from properties.api.permissions import CanSubmitProperty
from properties.models import PropertySubmission
from properties.selectors import (
    get_user_submission,
    get_user_submissions,
)

from properties.api.serializers.submission.detail import PropertySubmissionDetailSerializer
from properties.api.serializers.submission.input import CreatePropertySubmissionSerializer, UpdatePropertySubmissionSerializer
from properties.api.serializers.submission.list import PropertySubmissionListSerializer
from properties.services import (
    archive_submission_draft,
    create_submission_draft,
    submit_property_submission,
    update_submission_draft,
)


# =====================================================
# VALIDATION ERROR FORMATTER
# =====================================================
def format_django_validation_error(exc):
    """
    Converts Django's ValidationError into an API-friendly dictionary.
    """

    if hasattr(exc, "message_dict"):
        return exc.message_dict

    if hasattr(exc, "messages"):
        return {
            "non_field_errors": exc.messages,
        }

    return {
        "non_field_errors": [str(exc)],
    }


# =====================================================
# CREATE AND LIST PROPERTY SUBMISSIONS
# =====================================================
class PropertySubmissionListCreateAPIView(APIView):
    """
    Creates a property-submission draft or lists the authenticated
    user's existing submissions.
    """

    permission_classes = [
        IsAuthenticated,
        CanSubmitProperty,
    ]

    # =================================================
    # LIST USER SUBMISSIONS
    # =================================================
    @extend_schema(
        tags=["Property Submissions"],
        summary="List property submissions",
        description=(
            "Return all non-archived property submissions belonging "
            "to the authenticated user."
        ),
        responses={
            200: PropertySubmissionListSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            403: OpenApiResponse(
                description="Account cannot submit properties.",
            ),
        },
    )
    def get(self, request):
        submissions = get_user_submissions(
            user=request.user,
        )

        serializer = PropertySubmissionListSerializer(
            submissions,
            many=True,
        )

        return success_response(
            message="Property submissions retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    # =================================================
    # CREATE SUBMISSION DRAFT
    # =================================================
    @extend_schema(
        tags=["Property Submissions"],
        summary="Create property submission draft",
        description=(
            "Create an incomplete property submission draft. "
            "All fields are optional because the submission may be "
            "completed through a multi-step frontend form."
        ),
        request=CreatePropertySubmissionSerializer,
        responses={
            201: PropertySubmissionDetailSerializer,
            400: OpenApiResponse(
                description="Invalid submission data.",
            ),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            403: OpenApiResponse(
                description="Account cannot submit properties.",
            ),
        },
    )
    def post(self, request):
        serializer = CreatePropertySubmissionSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid property submission data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = dict(serializer.validated_data)

        amenities = validated_data.pop(
            "amenities",
            None,
        )

        try:
            submission = create_submission_draft(
                user=request.user,
                data=validated_data,
                amenities=amenities,
            )

        except DjangoValidationError as exc:
            return error_response(
                message="Unable to create property submission.",
                errors=format_django_validation_error(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = PropertySubmissionDetailSerializer(
            submission,
        )

        return success_response(
            message="Property submission draft created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


# =====================================================
# RETRIEVE AND UPDATE PROPERTY SUBMISSION
# =====================================================
class PropertySubmissionDetailAPIView(APIView):
    """
    Retrieves or updates a property submission belonging to the
    authenticated user.
    """

    permission_classes = [
        IsAuthenticated,
        CanSubmitProperty,
    ]

    # =================================================
    # INTERNAL SUBMISSION LOOKUP
    # =================================================
    def get_submission(self, *, request, submission_uuid):
        try:
            return get_user_submission(
                user=request.user,
                submission_uuid=submission_uuid,
            )

        except PropertySubmission.DoesNotExist:
            return None

    # =================================================
    # RETRIEVE SUBMISSION
    # =================================================
    @extend_schema(
        tags=["Property Submissions"],
        summary="Retrieve property submission",
        description=(
            "Retrieve one non-archived property submission belonging "
            "to the authenticated user."
        ),
        responses={
            200: PropertySubmissionDetailSerializer,
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def get(self, request, submission_uuid):
        submission = self.get_submission(
            request=request,
            submission_uuid=submission_uuid,
        )

        if submission is None:
            return error_response(
                message="Property submission not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = PropertySubmissionDetailSerializer(
            submission,
        )

        return success_response(
            message="Property submission retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    # =================================================
    # UPDATE SUBMISSION DRAFT
    # =================================================
    @extend_schema(
        tags=["Property Submissions"],
        summary="Update property submission draft",
        description=(
            "Partially update a draft submission or a submission "
            "returned for more information."
        ),
        request=UpdatePropertySubmissionSerializer,
        responses={
            200: PropertySubmissionDetailSerializer,
            400: OpenApiResponse(
                description="Invalid submission data.",
            ),
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def patch(self, request, submission_uuid):
        submission = self.get_submission(
            request=request,
            submission_uuid=submission_uuid,
        )

        if submission is None:
            return error_response(
                message="Property submission not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = UpdatePropertySubmissionSerializer(
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return error_response(
                message="Invalid property submission data.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = dict(serializer.validated_data)

        # Important:
        # Missing amenities means keep existing selections.
        # An empty list means remove all amenities.
        amenities = (
            validated_data.pop("amenities")
            if "amenities" in validated_data
            else None
        )

        try:
            submission = update_submission_draft(
                submission=submission,
                user=request.user,
                data=validated_data,
                amenities=amenities,
            )

        except DjangoValidationError as exc:
            return error_response(
                message="Unable to update property submission.",
                errors=format_django_validation_error(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = PropertySubmissionDetailSerializer(
            submission,
        )

        return success_response(
            message="Property submission updated successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# SUBMIT PROPERTY FOR REVIEW
# =====================================================
class SubmitPropertySubmissionAPIView(APIView):
    """
    Transitions a completed property submission from DRAFT or
    MORE_INFORMATION_REQUIRED to SUBMITTED.
    """

    permission_classes = [
        IsAuthenticated,
        CanSubmitProperty,
    ]

    @extend_schema(
        tags=["Property Submissions"],
        summary="Submit property for review",
        description=(
            "Validate the completed property submission and place it "
            "in the administrative review queue."
        ),
        request=None,
        responses={
            200: PropertySubmissionDetailSerializer,
            400: OpenApiResponse(
                description=(
                    "Submission is incomplete or cannot be submitted."
                ),
            ),
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def post(self, request, submission_uuid):
        try:
            submission = get_user_submission(
                user=request.user,
                submission_uuid=submission_uuid,
            )

        except PropertySubmission.DoesNotExist:
            return error_response(
                message="Property submission not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            submission = submit_property_submission(
                submission=submission,
                user=request.user,
            )

        except DjangoValidationError as exc:
            return error_response(
                message="Property submission could not be submitted.",
                errors=format_django_validation_error(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PropertySubmissionDetailSerializer(
            submission,
        )

        return success_response(
            message="Property submitted for review successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# ARCHIVE PROPERTY SUBMISSION
# =====================================================
class ArchivePropertySubmissionAPIView(APIView):
    """
    Soft-archives a property-submission draft.
    """

    permission_classes = [
        IsAuthenticated,
        CanSubmitProperty,
    ]

    @extend_schema(
        tags=["Property Submissions"],
        summary="Archive property submission draft",
        description=(
            "Archive a draft submission instead of permanently "
            "deleting it."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="Submission archived successfully.",
            ),
            400: OpenApiResponse(
                description="Submission cannot be archived.",
            ),
            404: OpenApiResponse(
                description="Property submission not found.",
            ),
        },
    )
    def delete(self, request, submission_uuid):
        try:
            submission = get_user_submission(
                user=request.user,
                submission_uuid=submission_uuid,
            )

        except PropertySubmission.DoesNotExist:
            return error_response(
                message="Property submission not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            archive_submission_draft(
                submission=submission,
                user=request.user,
            )

        except DjangoValidationError as exc:
            return error_response(
                message="Property submission could not be archived.",
                errors=format_django_validation_error(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Property submission archived successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
        )