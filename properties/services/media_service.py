# =====================================================
# PROPERTY SUBMISSION MEDIA SERVICE
# =====================================================

from decimal import Decimal
from pathlib import Path
from typing import Any

import logging
from typing import Any


import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
from django.db import transaction
from django.db.models import Max
from properties.models.property.submission import PropertySubmission
from properties.models.property.media import PropertySubmissionMedia

logger = logging.getLogger(__name__)

# =====================================================
# MEDIA SERVICE EXCEPTIONS
# =====================================================


class PropertySubmissionMediaError(Exception):
    """
    Base exception for property-submission media operations.
    """


class PropertySubmissionMediaUploadError(PropertySubmissionMediaError):
    """
    Raised when Cloudinary cannot upload the file.
    """


class PropertySubmissionMediaSaveError(PropertySubmissionMediaError):
    """
    Raised when uploaded media metadata cannot be saved.
    """


# =====================================================
# CLOUDINARY FOLDER
# =====================================================


def get_submission_media_folder(
    *,
    submission: PropertySubmission,
) -> str:
    """
    Return the Cloudinary folder used for one property submission.
    """

    return "artishelta/" "property-submissions/" f"{submission.uuid}"


# =====================================================
# NEXT DISPLAY ORDER
# =====================================================


def get_next_media_display_order(
    *,
    submission: PropertySubmission,
) -> int:
    """
    Return the next display order for a submission's media.
    """

    highest_order = submission.media.aggregate(
        highest=Max("display_order"),
    ).get("highest")

    if highest_order is None:
        return 0

    return highest_order + 1


# =====================================================
# CLOUDINARY UPLOAD OPTIONS
# =====================================================


def build_cloudinary_upload_options(
    *,
    submission: PropertySubmission,
    media_type: str,
    original_filename: str,
) -> dict[str, Any]:
    """
    Build the upload options sent to Cloudinary.
    """

    filename_stem = Path(original_filename).stem.strip().lower().replace(" ", "-")

    resource_type = (
        "image" if media_type == PropertySubmissionMedia.MediaType.IMAGE else "video"
    )

    options: dict[str, Any] = {
        "folder": get_submission_media_folder(
            submission=submission,
        ),
        "resource_type": resource_type,
        "use_filename": True,
        "unique_filename": True,
        "overwrite": False,
        "filename_override": filename_stem,
        "context": {
            "submission_uuid": str(submission.uuid),
            "submitted_by": str(submission.submitted_by_id),
        },
    }

    if media_type == PropertySubmissionMedia.MediaType.IMAGE:
        options.update(
            {
                "quality": "auto",
                # "fetch_format": "auto",
            }
        )

    return options


# =====================================================
# CLOUDINARY UPLOAD
# =====================================================


def upload_file_to_cloudinary(
    *,
    submission: PropertySubmission,
    uploaded_file,
    media_type: str,
) -> dict[str, Any]:
    """
    Upload one validated image or video to Cloudinary.
    """

    options = build_cloudinary_upload_options(
        submission=submission,
        media_type=media_type,
        original_filename=uploaded_file.name,
    )

    logger.info(
        "Starting Cloudinary upload: "
        "filename=%s, media_type=%s, content_type=%s, "
        "size=%s, resource_type=%s",
        uploaded_file.name,
        media_type,
        getattr(uploaded_file, "content_type", ""),
        getattr(uploaded_file, "size", None),
        options.get("resource_type"),
    )

    try:
        result = cloudinary.uploader.upload(
            uploaded_file,
            **options,
        )

        print(result)

        logger.info(
            "Cloudinary upload successful: "
            "public_id=%s, resource_type=%s, bytes=%s",
            result.get("public_id"),
            result.get("resource_type"),
            result.get("bytes"),
        )


        return result

        # return result
        #         return cloudinary.uploader.upload(
        #             uploaded_file,
        #             **options,
        #         )

    except CloudinaryError as exc:
        logger.exception(
            "Cloudinary rejected the media upload."
        )

        raise PropertySubmissionMediaUploadError(
            f"Cloudinary upload failed: {exc}"
        ) from exc

    except Exception as exc:
        logger.exception(
            "Unexpected error during Cloudinary upload."
        )

        raise PropertySubmissionMediaUploadError(
            f"Unexpected media upload error: {exc}"
        ) from exc



# =====================================================
# DELETE CLOUDINARY RESOURCE
# =====================================================


def delete_cloudinary_resource(
    *,
    public_id: str,
    resource_type: str,
) -> None:
    """
    Delete an uploaded Cloudinary resource.

    Used as cleanup when database persistence fails.
    """

    if not public_id:
        return

    try:
        cloudinary.uploader.destroy(
            public_id,
            resource_type=resource_type,
            invalidate=True,
        )

    except CloudinaryError:
        # Cleanup failure should not hide the original exception.
        pass


# =====================================================
# NORMALIZE CLOUDINARY RESPONSE
# =====================================================


def build_media_model_data(
    *,
    submission: PropertySubmission,
    uploaded_file,
    media_type: str,
    cloudinary_result: dict[str, Any],
    caption: str = "",
    alt_text: str = "",
    is_cover: bool = False,
    display_order: int,
) -> dict[str, Any]:
    """
    Convert a Cloudinary upload response into model-ready data.
    """

    duration = cloudinary_result.get("duration")

    normalized_duration = Decimal(str(duration)) if duration is not None else None

    return {
        "submission": submission,
        "media_type": media_type,
        "upload_status": (PropertySubmissionMedia.UploadStatus.COMPLETED),
        "public_id": cloudinary_result["public_id"],
        "asset_id": cloudinary_result.get(
            "asset_id",
            "",
        ),
        "secure_url": cloudinary_result["secure_url"],
        "resource_type": cloudinary_result.get(
            "resource_type",
            media_type,
        ),
        "file_format": cloudinary_result.get(
            "format",
            "",
        ),
        "original_filename": cloudinary_result.get(
            "original_filename",
            uploaded_file.name,
        ),
        "content_type": getattr(
            uploaded_file,
            "content_type",
            "",
        ),
        "file_size": cloudinary_result.get(
            "bytes",
            uploaded_file.size,
        ),
        "width": cloudinary_result.get("width"),
        "height": cloudinary_result.get("height"),
        "duration": normalized_duration,
        "caption": caption,
        "alt_text": alt_text,
        "display_order": display_order,
        "is_cover": is_cover,
    }


# =====================================================
# CREATE SUBMISSION MEDIA
# =====================================================


@transaction.atomic
def create_submission_media(
    *,
    submission: PropertySubmission,
    user,
    uploaded_file,
    media_type: str,
    caption: str = "",
    alt_text: str = "",
    is_cover: bool = False,
) -> PropertySubmissionMedia:
    """
    Upload one file to Cloudinary and save its metadata.

    The first uploaded image becomes the cover automatically.
    """

    locked_submission = PropertySubmission.objects.select_for_update().get(
        pk=submission.pk
    )

    if locked_submission.submitted_by_id != user.id:
        raise PropertySubmissionMediaError("You do not own this property submission.")

    if locked_submission.status not in {
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
    }:
        raise PropertySubmissionMediaError(
            "Media can only be added to an editable property submission."
        )

    next_display_order = get_next_media_display_order(
        submission=locked_submission,
    )

    if media_type == PropertySubmissionMedia.MediaType.IMAGE:
        image_exists = locked_submission.media.filter(
            media_type=(PropertySubmissionMedia.MediaType.IMAGE),
            upload_status=(PropertySubmissionMedia.UploadStatus.COMPLETED),
        ).exists()

        if not image_exists:
            is_cover = True

    if media_type == PropertySubmissionMedia.MediaType.VIDEO:
        is_cover = False

    cloudinary_result = upload_file_to_cloudinary(
        submission=locked_submission,
        uploaded_file=uploaded_file,
        media_type=media_type,
    )

    public_id = cloudinary_result.get(
        "public_id",
        "",
    )

    resource_type = cloudinary_result.get(
        "resource_type",
        media_type,
    )

    try:
        if is_cover:
            locked_submission.media.filter(
                media_type=(PropertySubmissionMedia.MediaType.IMAGE),
                is_cover=True,
            ).update(
                is_cover=False,
            )

        media_data = build_media_model_data(
            submission=locked_submission,
            uploaded_file=uploaded_file,
            media_type=media_type,
            cloudinary_result=cloudinary_result,
            caption=caption,
            alt_text=alt_text,
            is_cover=is_cover,
            display_order=next_display_order,
        )

        media = PropertySubmissionMedia.objects.create(
            **media_data,
        )

    except Exception as exc:
        delete_cloudinary_resource(
            public_id=public_id,
            resource_type=resource_type,
        )

        raise PropertySubmissionMediaSaveError(
            "The media was uploaded, but its metadata could not be saved."
        ) from exc

    return media


# =====================================================
# GET OWNED SUBMISSION MEDIA
# =====================================================


def get_owned_submission_media(
    *,
    submission: PropertySubmission,
    media_uuid,
) -> PropertySubmissionMedia:
    """
    Return one media record belonging to the supplied submission.
    """

    try:
        return PropertySubmissionMedia.objects.get(
            uuid=media_uuid,
            submission=submission,
        )

    except PropertySubmissionMedia.DoesNotExist as exc:
        raise PropertySubmissionMediaError("Property media was not found.") from exc


# =====================================================
# DELETE SUBMISSION MEDIA
# =====================================================


@transaction.atomic
def delete_submission_media(
    *,
    submission: PropertySubmission,
    user,
    media_uuid,
) -> None:
    """
    Delete one property-submission media record from Cloudinary
    and PostgreSQL.

    If the deleted media is the cover image, the next available
    completed image becomes the new cover.
    """

    locked_submission = PropertySubmission.objects.select_for_update().get(
        pk=submission.pk
    )

    if locked_submission.submitted_by_id != user.id:
        raise PropertySubmissionMediaError("You do not own this property submission.")

    if locked_submission.status not in {
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
    }:
        raise PropertySubmissionMediaError(
            "Media can only be deleted from an editable submission."
        )

    try:
        media = PropertySubmissionMedia.objects.select_for_update().get(
            uuid=media_uuid,
            submission=locked_submission,
        )

    except PropertySubmissionMedia.DoesNotExist as exc:
        raise PropertySubmissionMediaError("Property media was not found.") from exc

    was_cover = media.is_cover
    public_id = media.public_id
    resource_type = media.resource_type

    try:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type=resource_type,
            invalidate=True,
        )

    except CloudinaryError as exc:
        raise PropertySubmissionMediaError(
            f"Unable to delete media from Cloudinary: {exc}"
        ) from exc

    deletion_result = result.get("result")

    if deletion_result not in {
        "ok",
        "not found",
    }:
        raise PropertySubmissionMediaError("Cloudinary could not delete the media.")

    media.delete()

    if was_cover:
        replacement_cover = (
            locked_submission.media.filter(
                media_type=PropertySubmissionMedia.MediaType.IMAGE,
                upload_status=PropertySubmissionMedia.UploadStatus.COMPLETED,
            )
            .order_by(
                "display_order",
                "created_at",
            )
            .first()
        )

        if replacement_cover:
            replacement_cover.is_cover = True

            replacement_cover.save(
                update_fields=[
                    "is_cover",
                    "updated_at",
                ]
            )


# =====================================================
# SET COVER IMAGE
# =====================================================


@transaction.atomic
def set_submission_cover_media(
    *,
    submission: PropertySubmission,
    user,
    media_uuid,
) -> PropertySubmissionMedia:
    """
    Mark one completed image as the cover image.

    Videos cannot be selected as cover media.
    """

    locked_submission = PropertySubmission.objects.select_for_update().get(
        pk=submission.pk
    )

    if locked_submission.submitted_by_id != user.id:
        raise PropertySubmissionMediaError("You do not own this property submission.")

    if locked_submission.status not in {
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
    }:
        raise PropertySubmissionMediaError(
            "The cover image can only be changed on an editable submission."
        )

    try:
        media = PropertySubmissionMedia.objects.select_for_update().get(
            uuid=media_uuid,
            submission=locked_submission,
            upload_status=PropertySubmissionMedia.UploadStatus.COMPLETED,
        )

    except PropertySubmissionMedia.DoesNotExist as exc:
        raise PropertySubmissionMediaError("Property media was not found.") from exc

    if media.media_type != PropertySubmissionMedia.MediaType.IMAGE:
        raise PropertySubmissionMediaError(
            "Only an image can be selected as the cover."
        )

    locked_submission.media.filter(
        media_type=PropertySubmissionMedia.MediaType.IMAGE,
        is_cover=True,
    ).exclude(
        pk=media.pk,
    ).update(
        is_cover=False,
    )

    if not media.is_cover:
        media.is_cover = True

        media.save(
            update_fields=[
                "is_cover",
                "updated_at",
            ]
        )

    return media
