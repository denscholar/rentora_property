from django.db import transaction
from django.utils import timezone

from properties.models.property.submission import PropertySubmission
from property_verification.models import PropertyVerification

from property_verification.services.property_verification_workflow import (
    PropertyVerificationWorkflow,
)


class PropertyVerificationAdminService:
    """
    Handles internal SheltaMe verification decisions.
    """

    @classmethod
    @transaction.atomic
    def verify(
        cls,
        *,
        verification,
        reviewer,
        review_note="",
    ):
        """
        Final verification decision by SheltaMe staff.
        """

        if (
            verification.submission.status
            != PropertyVerification.VerificationStatus.UNDER_REVIEW
        ):
            raise ValueError(
                "Only verification cases under review can be verified."
            )

        return PropertyVerificationWorkflow.transition(
            verification=verification,
            new_status=(
                PropertyVerification.VerificationStatus.VERIFIED
            ),
            # reviewed_by=reviewer,
            # review_note=review_note,
        )

    @classmethod
    @transaction.atomic
    def reject(
        cls,
        *,
        verification,
        reviewer,
        review_note,
    ):
        """
        Final rejection decision by SheltaMe staff.
        """

        if (
            verification.submission.status
            != PropertyVerification.VerificationStatus.UNDER_REVIEW
        ):

            raise ValueError(
                "Only verification cases under review can be rejected."
            )

        if not review_note.strip():
            raise ValueError(
                "A rejection reason is required."
            )

        return PropertyVerificationWorkflow.transition(
            verification=verification,
            new_status=(
                PropertyVerification.VerificationStatus.REJECTED
            ),
        )




class PropertySubmissionModerationService:
    """
    Handles internal SheltaMe moderation of property submissions.

    This service owns:
        - approval
        - rejection
        - moderation notes
        - reviewer information
        - moderation timestamps
    """

    @classmethod
    @transaction.atomic
    def approve(
        cls,
        *,
        submission,
        reviewer,
        review_note="",
    ):
        """
        Approve a property submission currently under review.
        """

        if (
            submission.status
            != PropertySubmission.Status.UNDER_REVIEW
        ):
  
            raise ValueError(
                "Only property submissions under review can be approved."
            )

        now = timezone.now()

        submission.status = PropertySubmission.Status.APPROVED
        submission.reviewed_by = reviewer
        submission.reviewed_at = now
        submission.review_note = review_note.strip()


        submission.save(
            update_fields=[
                "status",
                "reviewed_by",
                "reviewed_at",
                "review_note",
                "updated_at",
            ]
        )

        return submission

    @classmethod
    @transaction.atomic
    def reject(
        cls,
        *,
        submission,
        reviewer,
        review_note,
    ):
        """
        Reject a property submission currently under review.
        """

        if (
            submission.status
            != PropertySubmission.Status.UNDER_REVIEW
        ):
            raise ValueError(
                "Only property submissions under review can be rejected."
            )

        review_note = review_note.strip()

        if not review_note:
            raise ValueError(
                "A rejection reason is required."
            )

        now = timezone.now()

        submission.status = PropertySubmission.Status.REJECTED
        submission.reviewed_by = reviewer
        submission.reviewed_at = now
        submission.review_note = review_note

        submission.save(
            update_fields=[
                "status",
                "reviewed_by",
                "reviewed_at",
                "review_note",
                "updated_at",
            ]
        )

        return submission