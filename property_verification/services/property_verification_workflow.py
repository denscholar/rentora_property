from django.db import transaction
from django.utils import timezone

from property_verification.models import PropertyVerification


class PropertyVerificationWorkflow:
    """
    Handles valid state transitions for PropertyVerification.
    """

    ALLOWED_TRANSITIONS = {
        PropertyVerification.VerificationStatus.PENDING: {
            PropertyVerification.VerificationStatus.AUTHORIZATION_SENT,
            PropertyVerification.VerificationStatus.CANCELLED,
        },
        PropertyVerification.VerificationStatus.AUTHORIZATION_SENT: {
            PropertyVerification.VerificationStatus.AUTHORIZED,
            PropertyVerification.VerificationStatus.REJECTED,
            PropertyVerification.VerificationStatus.EXPIRED,
            PropertyVerification.VerificationStatus.CANCELLED,
        },
        PropertyVerification.VerificationStatus.AUTHORIZED: {
            PropertyVerification.VerificationStatus.UNDER_REVIEW,
            PropertyVerification.VerificationStatus.REJECTED,
            PropertyVerification.VerificationStatus.CANCELLED,
            PropertyVerification.VerificationStatus.VERIFIED,
        },
        PropertyVerification.VerificationStatus.UNDER_REVIEW: {
            PropertyVerification.VerificationStatus.VERIFIED,
            PropertyVerification.VerificationStatus.REJECTED,
        },
        PropertyVerification.VerificationStatus.VERIFIED: set(),
        PropertyVerification.VerificationStatus.REJECTED: set(),
        PropertyVerification.VerificationStatus.EXPIRED: set(),
        PropertyVerification.VerificationStatus.CANCELLED: set(),
    }

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        verification,
        new_status,
    ):
        current_status = verification.status

        if current_status == PropertyVerification.VerificationStatus.VERIFIED:
            raise ValueError(("Property already verified"))

        allowed_statuses = cls.ALLOWED_TRANSITIONS.get(
            current_status,
            set(),
        )

        if new_status not in allowed_statuses:
            raise ValueError(
                (
                    f"Invalid verification transition: "
                    f"{current_status} → {new_status}"
                )
            )

        verification.status = new_status

        now = timezone.now()

        if new_status == PropertyVerification.VerificationStatus.AUTHORIZED:

            verification.authorized_at = now

        elif new_status == PropertyVerification.VerificationStatus.VERIFIED:
            verification.verified_at = now

        elif new_status == PropertyVerification.VerificationStatus.REJECTED:
            verification.rejected_at = now

        verification.save(
            update_fields=[
                "status",
                "authorized_at",
                "verified_at",
                "rejected_at",
                "updated_at",
            ]
        )

        return verification

    @classmethod
    @transaction.atomic
    def submit_for_review(cls, verification):
        cls.validate_ready_for_review(verification)

        return cls.transition(
            verification=verification,
            new_status=(PropertyVerification.VerificationStatus.UNDER_REVIEW),
        )

    @classmethod
    def validate_ready_for_review(cls, verification):
        """
        Validates whether a verification is ready
        to enter admin review.
        """

        if verification.status != PropertyVerification.VerificationStatus.AUTHORIZED:
            raise ValueError(
                "Only an authorized verification can be submitted for review."
            )

        # We will connect this to the verification document
        # model once we confirm its exact structure.

        return True
