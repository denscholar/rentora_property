# =====================================================
# PROPERTY SUBMISSION MEDIA SERIALIZERS
# =====================================================

from pathlib import Path

from rest_framework import serializers

from properties.models import (
    PropertySubmission,
    PropertySubmissionMedia,
)


# =====================================================
# MEDIA LIMITS
# =====================================================

MAX_IMAGES_PER_SUBMISSION = 10
MAX_VIDEOS_PER_SUBMISSION = 1

MAX_IMAGE_SIZE = 8 * 1024 * 1024
MAX_VIDEO_SIZE = 100 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".webm",
}

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

ALLOWED_VIDEO_CONTENT_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/webm",
}


# =====================================================
# MEDIA UPLOAD INPUT SERIALIZER
# =====================================================

class PropertySubmissionMediaUploadSerializer(
    serializers.Serializer
):
    """
    Validates an image or video before it is uploaded to Cloudinary.
    """

    file = serializers.FileField(
        required=True,
        write_only=True,
    )

    media_type = serializers.ChoiceField(
        choices=PropertySubmissionMedia.MediaType.choices,
        required=True,
    )

    caption = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )

    alt_text = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )

    is_cover = serializers.BooleanField(
        required=False,
        default=False,
    )

    def validate_file(self, uploaded_file):
        extension = Path(
            uploaded_file.name
        ).suffix.lower()

        content_type = getattr(
            uploaded_file,
            "content_type",
            "",
        )

        if not extension:
            raise serializers.ValidationError(
                "The uploaded file must have a valid extension."
            )

        uploaded_file._validated_extension = extension
        uploaded_file._validated_content_type = content_type

        return uploaded_file

    def validate(self, attrs):
        uploaded_file = attrs["file"]
        media_type = attrs["media_type"]

        extension = getattr(
            uploaded_file,
            "_validated_extension",
            Path(uploaded_file.name).suffix.lower(),
        )

        content_type = getattr(
            uploaded_file,
            "_validated_content_type",
            getattr(uploaded_file, "content_type", ""),
        )

        if media_type == PropertySubmissionMedia.MediaType.IMAGE:
            self._validate_image(
                uploaded_file=uploaded_file,
                extension=extension,
                content_type=content_type,
            )

        if media_type == PropertySubmissionMedia.MediaType.VIDEO:
            self._validate_video(
                uploaded_file=uploaded_file,
                extension=extension,
                content_type=content_type,
            )

        submission = self.context.get("submission")

        if submission is not None:
            self._validate_submission(
                submission=submission,
                media_type=media_type,
                is_cover=attrs.get("is_cover", False),
            )

        return attrs

    def _validate_image(
        self,
        *,
        uploaded_file,
        extension,
        content_type,
    ):
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(
                {
                    "file": (
                        "Image files must be JPG, JPEG, PNG, or WEBP."
                    )
                }
            )

        if (
            content_type
            and content_type not in ALLOWED_IMAGE_CONTENT_TYPES
        ):
            raise serializers.ValidationError(
                {
                    "file": (
                        "The uploaded file content type is not a supported image."
                    )
                }
            )

        if uploaded_file.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError(
                {
                    "file": (
                        "Image size cannot exceed 8 MB."
                    )
                }
            )

    def _validate_video(
        self,
        *,
        uploaded_file,
        extension,
        content_type,
    ):
        if extension not in ALLOWED_VIDEO_EXTENSIONS:
            raise serializers.ValidationError(
                {
                    "file": (
                        "Video files must be MP4, MOV, or WEBM."
                    )
                }
            )

        if (
            content_type
            and content_type not in ALLOWED_VIDEO_CONTENT_TYPES
        ):
            raise serializers.ValidationError(
                {
                    "file": (
                        "The uploaded file content type is not a supported video."
                    )
                }
            )

        if uploaded_file.size > MAX_VIDEO_SIZE:
            raise serializers.ValidationError(
                {
                    "file": (
                        "Video size cannot exceed 100 MB."
                    )
                }
            )

    def _validate_submission(
        self,
        *,
        submission,
        media_type,
        is_cover,
    ):
        if submission.status not in {
            PropertySubmission.Status.DRAFT,
            # PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
        }:
            raise serializers.ValidationError(
                {
                    "submission": (
                        "Media can only be uploaded to an editable submission."
                    )
                }
            )

        media_queryset = submission.media.filter(
            upload_status=(
                PropertySubmissionMedia.UploadStatus.COMPLETED
            ),
        )

        if media_type == PropertySubmissionMedia.MediaType.IMAGE:
            image_count = media_queryset.filter(
                media_type=(
                    PropertySubmissionMedia.MediaType.IMAGE
                ),
            ).count()

            if image_count >= MAX_IMAGES_PER_SUBMISSION:
                raise serializers.ValidationError(
                    {
                        "file": (
                            "A property submission can have a maximum "
                            "of 10 images."
                        )
                    }
                )

        if media_type == PropertySubmissionMedia.MediaType.VIDEO:
            video_exists = media_queryset.filter(
                media_type=(
                    PropertySubmissionMedia.MediaType.VIDEO
                ),
            ).exists()

            if video_exists:
                raise serializers.ValidationError(
                    {
                        "file": (
                            "A property submission can have only one video."
                        )
                    }
                )

            if is_cover:
                raise serializers.ValidationError(
                    {
                        "is_cover": (
                            "A video cannot be used as the cover media."
                        )
                    }
                )


# =====================================================
# MEDIA OUTPUT SERIALIZER
# =====================================================

class PropertySubmissionMediaSerializer(
    serializers.ModelSerializer
):
    media_type_display = serializers.CharField(
        source="get_media_type_display",
        read_only=True,
    )

    class Meta:
        model = PropertySubmissionMedia

        fields = [
            "uuid",
            "media_type",
            "media_type_display",
            "upload_status",
            "public_id",
            "secure_url",
            "resource_type",
            "file_format",
            "original_filename",
            "content_type",
            "file_size",
            "width",
            "height",
            "duration",
            "caption",
            "alt_text",
            "display_order",
            "is_cover",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields