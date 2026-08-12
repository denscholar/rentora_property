from django.conf import settings
from django.db import models

from core.models import BaseModel
from properties.models.property.property_group import PropertyGroup
from properties.models.property.submission import PropertySubmission



class PropertyDuplicateCandidate(BaseModel):
    """
    Records a possible duplicate relationship between a submission
    and an existing canonical PropertyGroup.

    This model does NOT itself merge properties.

    It provides an auditable record of:
        - what submission was checked
        - which property group was considered
        - the matching score
        - why it was considered similar
        - how the candidate was resolved
    """

    class Status(models.TextChoices):
        PENDING = (
            "pending",
            "Pending Review",
        )
        MATCHED = (
            "matched",
            "Matched",
        )
        REJECTED = (
            "rejected",
            "Rejected",
        )
        IGNORED = (
            "ignored",
            "Ignored",
        )

    # =====================================================
    # SOURCE SUBMISSION
    # =====================================================

    submission = models.ForeignKey(
        PropertySubmission,
        on_delete=models.CASCADE,
        related_name="duplicate_candidates",
    )

    # =====================================================
    # POSSIBLE EXISTING PROPERTY
    # =====================================================

    property_group = models.ForeignKey(
        PropertyGroup,
        on_delete=models.CASCADE,
        related_name="duplicate_candidates",
    )

    # =====================================================
    # MATCH SCORE
    # =====================================================

    similarity_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text=(
            "Overall duplicate similarity score from 0 to 100."
        ),
    )

    # =====================================================
    # MATCHING INFORMATION
    # =====================================================

    matching_signals = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Individual signals that contributed to the "
            "similarity score."
        ),
    )

    conflicts = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            "Important differences found between the submission "
            "and the existing property."
        ),
    )

    # =====================================================
    # RESOLUTION
    # =====================================================

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="resolved_property_duplicates",
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    resolution_note = models.TextField(
        blank=True,
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:
        ordering = ["-similarity_score", "-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "submission",
                    "property_group",
                ],
                name="unique_submission_duplicate_candidate",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(similarity_score__gte=0)
                    & models.Q(similarity_score__lte=100)
                ),
                name="dup_candidate_score_0_100",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "submission",
                    "status",
                ],
                name="dup_candidate_submission_idx",
            ),
            models.Index(
                fields=[
                    "property_group",
                    "status",
                ],
                name="dup_candidate_property_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "-similarity_score",
                ],
                name="dup_candidate_review_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.submission} → "
            f"{self.property_group} "
            f"({self.similarity_score}%)"
        )