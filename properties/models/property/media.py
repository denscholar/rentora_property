# =====================================================
# PROPERTY SUBMISSION MEDIA MODEL
# =====================================================
from django.db import models
from core.models import BaseModel


# =====================================================
# PROPERTY SUBMISSION MEDIA
# =====================================================
class PropertySubmissionMedia(BaseModel):
    """
    Stores Cloudinary metadata for an image or video uploaded
    for a property submission.

    The actual file is stored in Cloudinary. PostgreSQL stores
    only the Cloudinary identifiers, delivery URL and metadata.
    """

    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    class UploadStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    submission = models.ForeignKey(
        "properties.PropertySubmission",
        on_delete=models.CASCADE,
        related_name="media",
    )

    media_type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
        db_index=True,
    )

    upload_status = models.CharField(
        max_length=20,
        choices=UploadStatus.choices,
        default=UploadStatus.COMPLETED,
        db_index=True,
    )

    # Cloudinary's unique identifier for the uploaded resource.
    public_id = models.CharField(
        max_length=500,
        unique=True,
        db_index=True,
    )

    # Cloudinary asset identifier. This normally remains stable
    # even when the resource is renamed.
    asset_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    # Public HTTPS delivery URL returned by Cloudinary.
    secure_url = models.URLField(
        max_length=1000,
    )

    # Cloudinary resource type: image, video or raw.
    resource_type = models.CharField(
        max_length=30,
    )

    # Cloudinary file format: jpg, png, webp, mp4, etc.
    file_format = models.CharField(
        max_length=30,
        blank=True,
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True,
    )

    content_type = models.CharField(
        max_length=100,
        blank=True,
    )

    file_size = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        help_text="File size in bytes.",
    )

    width = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    height = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    duration = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Video duration in seconds.",
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Accessible description of the image.",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
    )

    is_cover = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "submission",
                    "media_type",
                ],
                name="sub_media_type_idx",
            ),
            models.Index(
                fields=[
                    "submission",
                    "display_order",
                ],
                name="sub_media_order_idx",
            ),
            models.Index(
                fields=[
                    "submission",
                    "upload_status",
                ],
                name="sub_media_status_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["submission"],
                condition=models.Q(
                    is_cover=True,
                    media_type="image",
                ),
                name="one_cover_image_per_submission",
            ),
        ]

    @property
    def is_image(self) -> bool:
        return (
            self.media_type
            == self.MediaType.IMAGE
        )

    @property
    def is_video(self) -> bool:
        return (
            self.media_type
            == self.MediaType.VIDEO
        )

    def __str__(self):
        filename = (
            self.original_filename
            or self.public_id
        )

        return (
            f"{filename} - "
            f"{self.get_media_type_display()}"
        )