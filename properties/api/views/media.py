# =====================================================
# PROPERTY SUBMISSION MEDIA API VIEWS
# =====================================================

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from properties.services.media_service import (
    delete_submission_media,
    set_submission_cover_media,
)


from core.api.responses import error_response, success_response
from properties.api.serializers.submission.media import (
    PropertySubmissionMediaSerializer,
    PropertySubmissionMediaUploadSerializer,
)
from properties.models.property.submission import PropertySubmission
from properties.selectors.submission_selector import get_user_submission
from properties.services import (
    PropertySubmissionMediaError,
    PropertySubmissionMediaSaveError,
    PropertySubmissionMediaUploadError,
    create_submission_media,
)


# =====================================================
# PROPERTY SUBMISSION MEDIA LIST AND UPLOAD
# =====================================================
class PropertySubmissionMediaListCreateAPIView(APIView):
    """
    List or upload media belonging to one property submission.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    # =================================================
    # LIST MEDIA
    # =================================================
    @extend_schema(
        tags=["Property Submission Media"],
        summary="List property submission media",
        description=(
            "Retrieve all completed images and videos uploaded "
            "for a property submission owned by the authenticated user."
        ),
        responses={
            200: PropertySubmissionMediaSerializer(
                many=True,
            ),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            404: OpenApiResponse(
                description=(
                    "Property submission was not found or does not "
                    "belong to the authenticated user."
                ),
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

        media = submission.media.filter(
            upload_status="completed",
        ).order_by(
            "display_order",
            "created_at",
        )

        serializer = PropertySubmissionMediaSerializer(
            media,
            many=True,
            context={
                "request": request,
            },
        )

        return success_response(
            message=("Property submission media retrieved successfully."),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    # =================================================
    # UPLOAD MEDIA
    # =================================================
    @extend_schema(
        tags=["Property Submission Media"],
        summary="Upload property submission media",
        description=(
            "Upload one image or video to Cloudinary for an editable "
            "property submission. The request must use multipart/form-data. "
            "The first uploaded image automatically becomes the cover image."
        ),
        request=PropertySubmissionMediaUploadSerializer,
        responses={
            201: PropertySubmissionMediaSerializer,
            400: OpenApiResponse(
                description=(
                    "Invalid file, unsupported media type, upload limit "
                    "reached, or submission is not editable."
                ),
            ),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            404: OpenApiResponse(
                description=(
                    "Property submission was not found or does not "
                    "belong to the authenticated user."
                ),
            ),
            502: OpenApiResponse(
                description="Cloudinary upload failed.",
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

        input_serializer = PropertySubmissionMediaUploadSerializer(
            data=request.data,
            context={
                "request": request,
                "submission": submission,
            },
        )

        if not input_serializer.is_valid():
            return error_response(
                message="Invalid property media data.",
                code="INVALID_PROPERTY_MEDIA",
                errors=input_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = input_serializer.validated_data

        try:
            media = create_submission_media(
                submission=submission,
                user=request.user,
                uploaded_file=validated_data["file"],
                media_type=validated_data["media_type"],
                caption=validated_data.get(
                    "caption",
                    "",
                ),
                alt_text=validated_data.get(
                    "alt_text",
                    "",
                ),
                is_cover=validated_data.get(
                    "is_cover",
                    False,
                ),
            )

        except PropertySubmissionMediaUploadError as exc:
            return error_response(
                message=str(exc),
                code="CLOUDINARY_UPLOAD_FAILED",
                status_code=status.HTTP_502_BAD_GATEWAY,
            )

        except PropertySubmissionMediaSaveError as exc:
            return error_response(
                message=str(exc),
                code="MEDIA_SAVE_FAILED",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except PropertySubmissionMediaError as exc:
            return error_response(
                message=str(exc),
                code="PROPERTY_MEDIA_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        output_serializer = PropertySubmissionMediaSerializer(
            media,
            context={
                "request": request,
            },
        )

        return success_response(
            message="Property media uploaded successfully.",
            code="PROPERTY_MEDIA_UPLOADED",
            data=output_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


# =====================================================
# DELETE PROPERTY SUBMISSION MEDIA
# =====================================================


class PropertySubmissionMediaDeleteAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Property Submission Media"],
        summary="Delete property submission media",
        description=(
            "Delete one image or video belonging to an editable property "
            "submission. The asset is deleted from Cloudinary before its "
            "metadata record is removed from the database."
        ),
        responses={
            200: OpenApiResponse(
                description="Property media deleted successfully.",
            ),
            400: OpenApiResponse(
                description=(
                    "The submission is not editable or the media "
                    "could not be deleted."
                ),
            ),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            404: OpenApiResponse(
                description=("The property submission or media record was not found."),
            ),
        },
    )
    def delete(
        self,
        request,
        submission_uuid,
        media_uuid,
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
            delete_submission_media(
                submission=submission,
                user=request.user,
                media_uuid=media_uuid,
            )

        except PropertySubmissionMediaError as exc:
            message = str(exc)

            response_status = (
                status.HTTP_404_NOT_FOUND
                if message == "Property media was not found."
                else status.HTTP_400_BAD_REQUEST
            )

            return error_response(
                message=message,
                code="PROPERTY_MEDIA_DELETE_FAILED",
                status_code=response_status,
            )

        return success_response(
            message="Property media deleted successfully.",
            code="PROPERTY_MEDIA_DELETED",
            data=None,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# SET PROPERTY SUBMISSION COVER IMAGE
# =====================================================


class PropertySubmissionMediaSetCoverAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Property Submission Media"],
        summary="Set property submission cover image",
        description=(
            "Select one completed image as the cover image for a property "
            "submission. Any previous cover image is automatically unset. "
            "Videos cannot be selected as cover media."
        ),
        request=None,
        responses={
            200: PropertySubmissionMediaSerializer,
            400: OpenApiResponse(
                description=(
                    "The media is not an image, the submission is not "
                    "editable, or the cover could not be updated."
                ),
            ),
            401: OpenApiResponse(
                description="Authentication required.",
            ),
            404: OpenApiResponse(
                description=("The property submission or media record was not found."),
            ),
        },
    )
    def post(
        self,
        request,
        submission_uuid,
        media_uuid,
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
            media = set_submission_cover_media(
                submission=submission,
                user=request.user,
                media_uuid=media_uuid,
            )

        except PropertySubmissionMediaError as exc:
            message = str(exc)

            response_status = (
                status.HTTP_404_NOT_FOUND
                if message == "Property media was not found."
                else status.HTTP_400_BAD_REQUEST
            )

            return error_response(
                message=message,
                code="PROPERTY_MEDIA_COVER_FAILED",
                status_code=response_status,
            )

        serializer = PropertySubmissionMediaSerializer(
            media,
            context={
                "request": request,
            },
        )

        return success_response(
            message="Property cover image updated successfully.",
            code="PROPERTY_MEDIA_COVER_UPDATED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
