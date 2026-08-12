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
from properties.api.pagination import PropertySubmissionPagination
from properties.api.permissions import CanSubmitProperty
from properties.models import PropertySubmission
from properties.selectors import (
    get_user_submission,
    get_user_submissions,
)

from properties.api.serializers.submission.detail import (
    PropertySubmissionDetailSerializer,
)
from properties.api.serializers.submission.input import (
    CreatePropertySubmissionSerializer,
    UpdatePropertySubmissionSerializer,
)
from properties.api.serializers.submission.list import PropertySubmissionListSerializer
from properties.services import (
    archive_submission_draft,
    create_submission_draft,
    submit_property_submission,
    update_submission_draft,
)
from properties.services.submission_service import PropertySubmissionSubmitError


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

    pagination_class = PropertySubmissionPagination

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
        # ---------------------------------------------------------
        # READ QUERY PARAMETERS
        # ---------------------------------------------------------
        search = request.query_params.get("search", "").strip()

        requested_status = request.query_params.get("status", "").strip().lower()

        # ---------------------------------------------------------
        # ALLOWED UI STATUSES
        # ---------------------------------------------------------

        allowed_statuses = {
            PropertySubmission.Status.DRAFT,
            PropertySubmission.Status.UNDER_REVIEW,
            PropertySubmission.Status.APPROVED,
            PropertySubmission.Status.REJECTED,
        }

        if requested_status and requested_status not in allowed_statuses:
            return error_response(
                message="Invalid property submission status.",
                errors={
                    "status": [
                        (
                            "Status must be one of: "
                            "draft, under_review, approved, rejected."
                        )
                    ]
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # ---------------------------------------------------------
        # BUILD QUERYSET
        # ---------------------------------------------------------
        submissions = get_user_submissions(
            user=request.user,
            status=requested_status or None,
            search=search or None,
        )

        paginator = self.pagination_class()

        page = paginator.paginate_queryset(
            submissions,
            request,
            view=self,
        )

        serializer = PropertySubmissionListSerializer(
            page,
            many=True,
            context={"request": request},
        )

        # ---------------------------------------------------------
        # RETURN PAGINATED RESPONSE
        # ---------------------------------------------------------

        paginated_data = paginator.get_paginated_data(
            serializer.data,
        )

        return success_response(
            message="Property submissions retrieved successfully.",
            data=paginated_data,
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
                uuid=submission_uuid,
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
            validated_data.pop("amenities") if "amenities" in validated_data else None
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
    permission_classes = [
        IsAuthenticated,
        CanSubmitProperty,
    ]

    @extend_schema(
        tags=["Property Submissions"],
        summary="Submit property for review",
        description=(
            "Validate and submit a completed property draft for review. "
            "The submission must contain the required property, location, "
            "pricing and media information."
        ),
        request=None,
        responses={
            200: PropertySubmissionDetailSerializer,
            400: OpenApiResponse(
                description=(
                    "The submission is incomplete or cannot be submitted "
                    "in its current status."
                ),
            ),
            401: OpenApiResponse(
                description="Authentication required.",
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

        try:
            submission = submit_property_submission(
                submission=submission,
                user=request.user,
            )

        except PropertySubmissionSubmitError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_SUBMISSION_INCOMPLETE",
                errors=getattr(
                    exc,
                    "errors",
                    None,
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PropertySubmissionDetailSerializer(
            submission,
            context={
                "request": request,
            },
        )

        return success_response(
            message=("Property submitted successfully and is now awaiting review."),
            code="PROPERTY_SUBMISSION_SUBMITTED",
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
            "Archive a draft submission instead of permanently " "deleting it."
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
                uuid=submission_uuid,
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
