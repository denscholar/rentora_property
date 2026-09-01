import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from properties.models.property.submission import PropertySubmission
from property_verification.models import (
    PropertyVerification,
    VerificationRepresentative,
)


class PropertyVerificationService:
    """
    Handles creation and initialization of a property verification case.

    This service owns:
        - verification creation
        - representative creation
        - secure invitation token generation
        - token hashing
        - token expiration
        - verification URL generation
    """

    INVITATION_EXPIRY_DAYS = 7

    # =========================================================
    # VERIFICATION STATE TRANSITIONS
    # =========================================================

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
    def validate_transition(cls, verification, new_status):
        """
        Validates whether a verification can move from its
        current status to the requested status.
        """

        current_status = verification.status

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

        if new_status == PropertyVerification.VerificationStatus.VERIFIED:
            submission = verification.submission

            if submission.status != submission.Status.APPROVED:
                raise ValueError(
                    (
                        "Property verification cannot be completed "
                        "until the property submission is approved."
                    )
                )

    @classmethod
    @transaction.atomic
    def initiate_verification(
        cls,
        *,
        submission,
        representative_name,
        representative_email,
        representative_role,
        representative_phone="",
        organization_name="",
    ):
        """
        Create a property verification case and its representative.

        Returns:
            tuple[PropertyVerification, str]

        The second value is the raw invitation token.
        The raw token is NEVER stored in the database.
        """

        # =========================================================
        # 1. Validate submission eligibility
        # =========================================================

        cls.validate_submission_for_verification(submission)

        # ---------------------------------------------------------
        # 1. Make sure the submission is eligible
        # ---------------------------------------------------------

        if submission.is_archived:
            raise ValueError("An archived property submission cannot be verified.")

        # ---------------------------------------------------------
        # 2. Prevent duplicate active verification cases
        # ---------------------------------------------------------

        existing_verification = getattr(
            submission,
            "verification",
            None,
        )

        if existing_verification is not None:
            if (
                existing_verification.status
                == PropertyVerification.VerificationStatus.VERIFIED
            ):
                raise ValueError("This property has already been verified.")

            if existing_verification.status in {
                PropertyVerification.VerificationStatus.AUTHORIZATION_SENT,
                PropertyVerification.VerificationStatus.UNDER_REVIEW,
                PropertyVerification.VerificationStatus.AUTHORIZED,
                PropertyVerification.VerificationStatus.VERIFIED,
            }:
                raise ValueError(
                    "This property already has an active verification request."
                )

        # ---------------------------------------------------------
        # 3. Generate secure invitation token
        # ---------------------------------------------------------

        raw_token = secrets.token_urlsafe(48)

        token_hash = cls._hash_token(raw_token)

        expires_at = timezone.now() + timedelta(days=cls.INVITATION_EXPIRY_DAYS)

        # ---------------------------------------------------------
        # 4. Create or reset verification
        # ---------------------------------------------------------

        verification = PropertyVerification.objects.create(
            submission=submission,
            status=PropertyVerification.VerificationStatus.AUTHORIZATION_SENT,
            token_hash=token_hash,
            token_expires_at=expires_at,
        )

        # ---------------------------------------------------------
        # 5. Create/update representative
        # ---------------------------------------------------------

        representative, _ = VerificationRepresentative.objects.update_or_create(
            verification=verification,
            defaults={
                "name": representative_name,
                "email": representative_email,
                "phone_number": representative_phone,
                "role": representative_role,
                "organization_name": organization_name,
                "confirmed_identity": False,
                "confirmed_authority": False,
            },
        )

        # ---------------------------------------------------------
        # 6. Record invitation time
        # ---------------------------------------------------------

        verification.authorization_sent_at = timezone.now()
        verification.save(
            update_fields=[
                "authorization_sent_at",
                "updated_at",
            ]
        )

        return verification, raw_token

    @classmethod
    def validate_submission_for_verification(cls, submission):
        """
        Raises ValueError when the submission cannot enter
        the property verification workflow.
        """

        if not cls.can_initiate_verification(submission):
            raise ValueError(
                "Property verification can only be requested "
                "for properties that are under review or approved."
            )

        return True

    # ============================================================
    # TOKEN HELPERS
    # ============================================================

    @staticmethod
    def _hash_token(token):
        """
        Hash the raw invitation token before storing it.
        """

        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @classmethod
    def verify_token(cls, token):
        """
        Resolve a valid invitation token to a verification record.

        Raises:
            ValueError if token is invalid, expired, or unusable.
        """

        if not token:
            raise ValueError("Verification token is required.")

        token_hash = cls._hash_token(token)

        try:
            verification = PropertyVerification.objects.select_related(
                "submission",
                "representative",
            ).get(
                token_hash=token_hash,
            )
        except PropertyVerification.DoesNotExist:
            raise ValueError("Invalid or expired verification invitation.")

        # ---------------------------------------------------------
        # Check expiry
        # ---------------------------------------------------------

        if verification.token_expires_at <= timezone.now():
            if verification.status not in {
                PropertyVerification.VerificationStatus.VERIFIED,
                PropertyVerification.VerificationStatus.REJECTED,
            }:
                verification.status = PropertyVerification.VerificationStatus.EXPIRED
                verification.save(
                    update_fields=[
                        "status",
                        "updated_at",
                    ]
                )

            raise ValueError("This verification invitation has expired.")

        # ---------------------------------------------------------
        # Check usable status
        # ---------------------------------------------------------

        if verification.status == PropertyVerification.VerificationStatus.AUTHORIZED:
            print(
                f"Verification ID={verification.id}, " f"Status={verification.status}"
            )
            raise ValueError("This verification link has already been used.")

        return verification

    # ============================================================
    # URL
    # ============================================================

    @classmethod
    def build_verification_url(cls, raw_token):
        """
        Build the URL sent to the landlord/representative.

        The raw token is only available at invitation creation time.
        """

        frontend_url = getattr(
            settings,
            "FRONTEND_URL",
            "http://localhost:3000",
        ).rstrip("/")

        return f"{frontend_url}" f"/property-verification/" f"{raw_token}"

    @classmethod
    def get_public_verification(cls, raw_token):
        """
        Resolve a public verification request from its
        secure invitation token.

        This method only validates and retrieves the verification.
        It does not authorize the property.
        """

        return cls.verify_token(raw_token)

    # =========================================================
    # SUBMISSION VERIFICATION ELIGIBILITY
    # =========================================================

    @classmethod
    def can_initiate_verification(cls, submission):
        """
        Determines whether a property submission is eligible
        to start the property verification workflow.

        Verification may be requested when the submission is:
            - UNDER_REVIEW
            - APPROVED
        """

        allowed_statuses = {
            PropertySubmission.Status.UNDER_REVIEW,
            PropertySubmission.Status.APPROVED,
        }

        return submission.status in allowed_statuses

    @classmethod
    def transition_status(
        cls,
        verification,
        new_status,
        *,
        reviewed_by=None,
        review_note="",
    ):
        cls.validate_transition(
            verification=verification,
            new_status=new_status,
        )

        now = timezone.now()

        # =====================================================
        # VERIFIED REQUIREMENT
        # =====================================================

        if new_status == PropertyVerification.VerificationStatus.VERIFIED:
            if verification.submission.status != PropertySubmission.Status.APPROVED:
                raise ValueError(
                    "This property cannot be verified until "
                    "the property submission has been approved."
                )

        # =====================================================
        # APPLY STATUS
        # =====================================================

        verification.status = new_status

        update_fields = [
            "status",
            "updated_at",
        ]

        # =====================================================
        # TIMESTAMPS
        # =====================================================

        if new_status == PropertyVerification.VerificationStatus.AUTHORIZATION_SENT:
            verification.authorization_sent_at = now

            update_fields.append("authorization_sent_at")

        elif new_status == PropertyVerification.VerificationStatus.AUTHORIZED:
            verification.authorized_at = now

            update_fields.append("authorized_at")

        elif new_status == PropertyVerification.VerificationStatus.VERIFIED:
            verification.verified_at = now

            update_fields.append("verified_at")

        elif new_status == PropertyVerification.VerificationStatus.REJECTED:
            verification.rejected_at = now

            update_fields.append("rejected_at")

        # =====================================================
        # ADMIN REVIEW INFORMATION
        # =====================================================

        if review_note:
            verification.review_note = review_note
            update_fields.append("review_note")

        if reviewed_by is not None:
            verification.reviewed_by = reviewed_by
            update_fields.append("reviewed_by")

        verification.save(update_fields=update_fields)

        return verification
