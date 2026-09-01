import logging
from pathlib import Path
from typing import Any
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
from django.db import transaction
from django.utils import timezone
from property_verification.exceptions import PropertyVerificationDocumentAuthorizationError, PropertyVerificationDocumentError, PropertyVerificationDocumentSaveError, PropertyVerificationDocumentUploadError
from property_verification.models import (
    PropertyVerification,
    PropertyVerificationDocument,
)

logger = logging.getLogger(__name__)




# ============================================================
# VERIFICATION STATUS
# ============================================================


def validate_verification_for_document_upload(
    *,
    verification: PropertyVerification,
) -> None:
    """
    Validate whether the verification is currently allowed
    to receive documents.
    """

    allowed_statuses = {
        PropertyVerification.VerificationStatus.PENDING,
        PropertyVerification.VerificationStatus.AUTHORIZATION_SENT,
        PropertyVerification.VerificationStatus.AUTHORIZED,
        PropertyVerification.VerificationStatus.UNDER_REVIEW,
    }

    if verification.status not in allowed_statuses:
        raise PropertyVerificationDocumentAuthorizationError(
            "Documents cannot be uploaded for this verification "
            f"because its current status is "
            f"'{verification.get_status_display()}'."
        )

    # --------------------------------------------------------
    # Token expiry
    # --------------------------------------------------------

    if (
        verification.token_expires_at
        and verification.token_expires_at <= timezone.now()
    ):
        raise PropertyVerificationDocumentAuthorizationError(
            "The property verification link has expired."
        )


# ============================================================
# CLOUDINARY FOLDER
# ============================================================


def get_verification_document_folder(
    *,
    verification: PropertyVerification,
) -> str:
    """
    Return the Cloudinary folder used for documents
    belonging to a property verification.
    """

    return "artishelta/" "property-verifications/" f"{verification.uuid}/" "documents"


# ============================================================
# CLOUDINARY UPLOAD OPTIONS
# ============================================================


def build_cloudinary_upload_options(
    *,
    verification: PropertyVerification,
    original_filename: str,
) -> dict[str, Any]:
    """
    Build Cloudinary upload options for a verification document.
    """

    filename_stem = Path(original_filename).stem.strip().lower().replace(" ", "-")

    return {
        "folder": get_verification_document_folder(
            verification=verification,
        ),
        "resource_type": "raw",
        "use_filename": True,
        "unique_filename": True,
        "overwrite": False,
        "filename_override": filename_stem,
        "context": {
            "verification_uuid": str(verification.uuid),
        },
    }


# ============================================================
# CLOUDINARY UPLOAD
# ============================================================


def upload_document_to_cloudinary(
    *,
    verification: PropertyVerification,
    uploaded_file,
) -> dict[str, Any]:
    """
    Upload one property verification document to Cloudinary.
    """

    options = build_cloudinary_upload_options(
        verification=verification,
        original_filename=uploaded_file.name,
    )

    logger.info(
        "Starting property verification document upload: "
        "verification=%s, filename=%s, content_type=%s, size=%s",
        verification.uuid,
        uploaded_file.name,
        getattr(
            uploaded_file,
            "content_type",
            "",
        ),
        getattr(
            uploaded_file,
            "size",
            None,
        ),
    )

    try:
        result = cloudinary.uploader.upload(
            uploaded_file,
            **options,
        )

        logger.info(
            "Property verification document uploaded successfully: "
            "verification=%s, public_id=%s, bytes=%s",
            verification.uuid,
            result.get("public_id"),
            result.get("bytes"),
        )

        return result

    except CloudinaryError as exc:
        logger.exception(
            "Cloudinary rejected the property verification " "document upload."
        )

        raise PropertyVerificationDocumentUploadError(
            f"Cloudinary upload failed: {exc}"
        ) from exc

    except Exception as exc:
        logger.exception(
            "Unexpected error during property verification " "document upload."
        )

        raise PropertyVerificationDocumentUploadError(
            f"Unexpected document upload error: {exc}"
        ) from exc


# ============================================================
# CLOUDINARY DELETE / CLEANUP
# ============================================================


def delete_cloudinary_document(
    *,
    public_id: str,
) -> None:
    """
    Delete an uploaded verification document from Cloudinary.

    This is primarily used when Cloudinary succeeds but the
    database operation fails.
    """

    if not public_id:
        return

    try:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="raw",
            invalidate=True,
        )

        logger.info(
            "Cloudinary verification document cleanup completed: "
            "public_id=%s, result=%s",
            public_id,
            result.get("result"),
        )

    except CloudinaryError:
        logger.exception(
            "Failed to cleanup Cloudinary verification document: " "public_id=%s",
            public_id,
        )

    except Exception:
        logger.exception(
            "Unexpected error during Cloudinary document cleanup: " "public_id=%s",
            public_id,
        )


# ============================================================
# CREATE DOCUMENT
# ============================================================


@transaction.atomic
def create_property_verification_document(
    *,
    verification: PropertyVerification,
    uploaded_file,
    document_type: str,
    uploaded_by_name: str = "",
) -> PropertyVerificationDocument:
    """
    Upload a property verification document to Cloudinary and
    persist the resulting metadata in PostgreSQL.
    """

    # --------------------------------------------------------
    # Lock verification
    # --------------------------------------------------------

    locked_verification = PropertyVerification.objects.select_for_update().get(
        pk=verification.pk,
    )

    # --------------------------------------------------------
    # Validate verification state
    # --------------------------------------------------------

    validate_verification_for_document_upload(
        verification=locked_verification,
    )

    # --------------------------------------------------------
    # Upload to Cloudinary
    # --------------------------------------------------------

    cloudinary_result = upload_document_to_cloudinary(
        verification=locked_verification,
        uploaded_file=uploaded_file,
    )

    public_id = cloudinary_result.get(
        "public_id",
        "",
    )

    # --------------------------------------------------------
    # Save metadata
    # --------------------------------------------------------

    try:
        document = PropertyVerificationDocument.objects.create(
            verification=locked_verification,
            document_type=document_type,
            public_id=public_id,
            secure_url=cloudinary_result["secure_url"],
            original_filename=(
                cloudinary_result.get(
                    "original_filename",
                    uploaded_file.name,
                )
            ),
            content_type=getattr(
                uploaded_file,
                "content_type",
                "",
            ),
            file_size=cloudinary_result.get(
                "bytes",
                uploaded_file.size,
            ),
            uploaded_by_name=uploaded_by_name,
        )

    except Exception as exc:

        # ----------------------------------------------------
        # Cloudinary succeeded but database failed.
        # Remove the orphaned Cloudinary resource.
        # ----------------------------------------------------

        delete_cloudinary_document(
            public_id=public_id,
        )

        logger.exception(
            "Failed to save property verification document "
            "metadata after successful Cloudinary upload."
        )

        raise PropertyVerificationDocumentSaveError(
            "The document was uploaded, but its metadata " "could not be saved."
        ) from exc


# ============================================================
# GET DOCUMENT
# ============================================================


def get_verification_document(
    *,
    verification: PropertyVerification,
    document_uuid,
) -> PropertyVerificationDocument:
    """
    Return one document belonging to the supplied verification.
    """

    try:
        return PropertyVerificationDocument.objects.get(
            uuid=document_uuid,
            verification=verification,
        )

    except PropertyVerificationDocument.DoesNotExist as exc:
        raise PropertyVerificationDocumentError(
            "Property verification document was not found."
        ) from exc


# ============================================================
# LIST DOCUMENTS
# ============================================================


def get_verification_documents(
    *,
    verification: PropertyVerification,
):
    """
    Return all documents belonging to a verification.
    """

    return PropertyVerificationDocument.objects.filter(
        verification=verification,
    ).order_by(
        "-created_at",
    )


# ============================================================
# DELETE DOCUMENT
# ============================================================


@transaction.atomic
def delete_property_verification_document(
    *,
    verification: PropertyVerification,
    document_uuid,
) -> None:
    """
    Delete a verification document from both Cloudinary
    and PostgreSQL.
    """

    locked_verification = PropertyVerification.objects.select_for_update().get(
        pk=verification.pk,
    )

    # --------------------------------------------------------
    # Verify state
    # --------------------------------------------------------

    validate_verification_for_document_upload(
        verification=locked_verification,
    )

    # --------------------------------------------------------
    # Get document
    # --------------------------------------------------------

    try:
        document = PropertyVerificationDocument.objects.select_for_update().get(
            uuid=document_uuid,
            verification=locked_verification,
        )

    except PropertyVerificationDocument.DoesNotExist as exc:
        raise PropertyVerificationDocumentError(
            "Property verification document was not found."
        ) from exc

    public_id = document.public_id

    # --------------------------------------------------------
    # Delete Cloudinary resource
    # --------------------------------------------------------

    try:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="raw",
            invalidate=True,
        )

    except CloudinaryError as exc:
        raise PropertyVerificationDocumentError(
            f"Unable to delete the document from Cloudinary: {exc}"
        ) from exc

    deletion_result = result.get(
        "result",
    )

    if deletion_result not in {
        "ok",
        "not found",
    }:
        raise PropertyVerificationDocumentError(
            "Cloudinary could not delete the document."
        )

    # --------------------------------------------------------
    # Delete database record
    # --------------------------------------------------------

    document.delete()
