import hashlib
import logging
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from property_verification.api.serializers.property_verification_document import (
    PropertyVerificationDocumentSerializer,
    PropertyVerificationDocumentUploadSerializer,
)
from property_verification.models import (
    PropertyVerification,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from property_verification.services.document_service import (
    PropertyVerificationDocumentAuthorizationError,
    PropertyVerificationDocumentError,
    PropertyVerificationDocumentSaveError,
    PropertyVerificationDocumentUploadError,
    create_property_verification_document,
    delete_property_verification_document,
    get_verification_documents,
)

logger = logging.getLogger(__name__)


# ============================================================
# TOKEN HASHING
# ============================================================


def hash_verification_token(
    token: str,
) -> str:
    """
    Hash the public verification token.

    IMPORTANT:
    This must match the hashing algorithm used when the
    PropertyVerification.token_hash was originally created.
    """

    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# ============================================================
# PUBLIC VERIFICATION LOOKUP
# ============================================================


def get_public_verification(
    *,
    verification_uuid,
    token,
):
    """
    Validate the public verification UUID + token pair and
    return the corresponding PropertyVerification.
    """

    try:
        verification = PropertyVerification.objects.get(
            uuid=verification_uuid,
        )

    except PropertyVerification.DoesNotExist:
        return None

    # --------------------------------------------------------
    # Token validation
    # --------------------------------------------------------

    token_hash = hash_verification_token(
        token,
    )

    if token_hash != verification.token_hash:
        return None

    # --------------------------------------------------------
    # Expiration
    # --------------------------------------------------------

    if (
        verification.token_expires_at
        and verification.token_expires_at <= timezone.now()
    ):
        return None

    return verification


# ============================================================
# PUBLIC DOCUMENT UPLOAD
# ============================================================


class PublicPropertyVerificationDocumentUploadAPIView(APIView):
    """
    Public endpoint used by a landlord or authorized
    representative to upload verification documents.
    """

    permission_classes = [
        AllowAny,
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @extend_schema(
        tags=["Property Verification"],
        summary="Upload verification document",
        description=(
            "Allows a landlord or authorized representative to upload "
            "supporting verification documents using a public verification link."
        ),
        request=PropertyVerificationDocumentUploadSerializer,
        responses={
            201: OpenApiResponse(
                description="Document uploaded successfully.",
            ),
            400: OpenApiResponse(
                description="Invalid upload request.",
            ),
            404: OpenApiResponse(
                description="Verification link is invalid or expired.",
            ),
            500: OpenApiResponse(
                description="Document save failed.",
            ),
            502: OpenApiResponse(
                description="Document upload provider error.",
            ),
        },
    )
    def post(
        self,
        request,
        verification_uuid,
        token,
    ):
        # ----------------------------------------------------
        # Verify public verification token
        # ----------------------------------------------------

        verification = get_public_verification(
            verification_uuid=verification_uuid,
            token=token,
        )

        if verification is None:
            return Response(
                {
                    "detail": ("The verification link is invalid " "or has expired."),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # Validate uploaded data
        # ----------------------------------------------------

        serializer = PropertyVerificationDocumentUploadSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        # ----------------------------------------------------
        # Get validated data
        # ----------------------------------------------------

        uploaded_file = serializer.validated_data["document"]

        document_type = serializer.validated_data["document_type"]

        # ----------------------------------------------------
        # Determine uploader name
        # ----------------------------------------------------

        uploaded_by_name = request.data.get(
            "uploaded_by_name",
            "",
        )

        # ----------------------------------------------------
        # Create document
        # ----------------------------------------------------

        try:
            document = create_property_verification_document(
                verification=verification,
                uploaded_file=uploaded_file,
                document_type=document_type,
                uploaded_by_name=uploaded_by_name,
            )

        except PropertyVerificationDocumentAuthorizationError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PropertyVerificationDocumentUploadError as exc:
            logger.exception("Property verification document upload failed.")

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except PropertyVerificationDocumentSaveError as exc:
            logger.exception("Property verification document database save failed.")

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except PropertyVerificationDocumentError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        response_serializer = PropertyVerificationDocumentSerializer(
            document,
        )

        return Response(
            {
                "message": ("Property verification document " "uploaded successfully."),
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class PublicPropertyVerificationDocumentListAPIView(APIView):
    """
    Return documents belonging to a public verification.
    """

    permission_classes = [
        AllowAny,
    ]

    @extend_schema(
        tags=["Property Verification"],
        summary="List verification documents",
        description=(
            "Returns all documents uploaded for a public property "
            "verification request."
        ),
        responses={
            200: OpenApiResponse(
                description="Documents retrieved successfully.",
            ),
            404: OpenApiResponse(
                description="Verification link is invalid or expired.",
            ),
        },
    )
    def get(
        self,
        request,
        verification_uuid,
        token,
    ):
        verification = get_public_verification(
            verification_uuid=verification_uuid,
            token=token,
        )

        if verification is None:
            return Response(
                {
                    "detail": ("The verification link is invalid " "or has expired."),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        documents = get_verification_documents(
            verification=verification,
        )

        serializer = PropertyVerificationDocumentSerializer(
            documents,
            many=True,
        )

        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class PublicPropertyVerificationDocumentDeleteAPIView(APIView):
    """
    Delete one document belonging to a public verification.
    """

    permission_classes = [
        AllowAny,
    ]

    @extend_schema(
        tags=["Property Verification"],
        summary="Delete verification document",
        description=(
            "Deletes a document associated with a public property "
            "verification request."
        ),
        responses={
            204: OpenApiResponse(
                description="Document deleted successfully.",
            ),
            400: OpenApiResponse(
                description="Document deletion failed.",
            ),
            404: OpenApiResponse(
                description="Verification link is invalid or expired.",
            ),
        },
    )
    def delete(
        self,
        request,
        verification_uuid,
        token,
        document_uuid,
    ):
        verification = get_public_verification(
            verification_uuid=verification_uuid,
            token=token,
        )

        if verification is None:
            return Response(
                {
                    "detail": ("The verification link is invalid " "or has expired."),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            delete_property_verification_document(
                verification=verification,
                document_uuid=document_uuid,
            )

        except PropertyVerificationDocumentError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": ("Property verification document " "deleted successfully."),
            },
            status=status.HTTP_204_NO_CONTENT,
        )
