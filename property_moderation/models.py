from django.db import models
from accounts.models import CustomUser
from core.models import BaseModel


import uuid

from django.conf import settings
from django.db import models


class PropertyModerationReview(BaseModel):

    class Decision(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        INFORMATION_REQUESTED = (
            "information_requested",
            "Information Requested",
        )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # =====================================================
    # SUBMISSION
    # =====================================================

    submission = models.ForeignKey(
        "properties.PropertySubmission",
        on_delete=models.PROTECT,
        related_name="moderation_reviews",
    )

    # =====================================================
    # MODERATOR
    # =====================================================

    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="property_moderation_actions",
        null=True,
        blank=True,
    )

    # =====================================================
    # DECISION
    # =====================================================

    decision = models.CharField(
        max_length=30,
        choices=Decision.choices,
        default=Decision.PENDING,
        db_index=True,
    )

    # =====================================================
    # MODERATOR FEEDBACK
    # =====================================================

    rejection_reason = models.TextField(
        blank=True,
        null=True,
    )

    information_request = models.TextField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    # =====================================================
    # META
    # =====================================================

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["decision", "-created_at"],
                name="mod_review_decision_idx",
            ),
            models.Index(
                fields=["submission", "-created_at"],
                name="mod_review_submission_idx",
            ),
        ]

    def __str__(self):
        return f"{self.submission_id} - " f"{self.get_decision_display()}"


class PropertyPublication(BaseModel):

    property_group = models.OneToOneField(
        "properties.PropertyGroup",
        on_delete=models.PROTECT,
        related_name="publication",
    )

    is_published = models.BooleanField(
        default=False,
        db_index=True,
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    unpublished_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    unpublished_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="property_publications_unpublished",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["is_published"],
                name="property_publication_live_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.property_group_id} - "
            f"{'Published' if self.is_published else 'Unpublished'}"
        )
