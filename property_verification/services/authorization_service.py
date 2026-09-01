from django.db import transaction
from django.utils import timezone

from property_verification.models import (
    PropertyVerification,
    PropertyVerificationAuthorization,
    VerificationRepresentative,
)


class PropertyVerificationAuthorizationService:
    """
    Handles the authorization/rejection response submitted by the
    landlord or authorized representative.
    """

    @staticmethod
    @transaction.atomic
    def respond(
        verification,
        *,
        decision,
        availability_confirmed=False,
        agent_authorized=False,
        authorization_note="",
        rejection_reason="",
        ip_address=None,
        user_agent="",
    ):
        now = timezone.now()

        # =====================================================
        # 1. VALIDATE DECISION
        # =====================================================

        allowed_decisions = {
            PropertyVerificationAuthorization.Decision.AUTHORIZED,
            PropertyVerificationAuthorization.Decision.REJECTED,
        }

        if decision not in allowed_decisions:
            raise ValueError("Invalid authorization decision.")

        # =====================================================
        # 2. VALIDATE STATUS
        # =====================================================

        allowed_statuses = {
            PropertyVerification.VerificationStatus.PENDING,
            PropertyVerification.VerificationStatus.AUTHORIZATION_SENT,
        }

        if verification.status not in allowed_statuses:
            raise ValueError(
                "This verification request is no longer " "available for authorization."
            )

        # =====================================================
        # 3. VALIDATE EXPIRY
        # =====================================================

        if verification.token_expires_at <= now:
            verification.status = PropertyVerification.VerificationStatus.EXPIRED

            verification.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            raise ValueError("This verification request has expired.")

        # =====================================================
        # 4. PREVENT DUPLICATE RESPONSE
        # =====================================================

        if PropertyVerificationAuthorization.objects.filter(
            verification=verification
        ).exists():
            raise ValueError(
                "This verification request has already " "received a response."
            )

        # =====================================================
        # 5. GET REPRESENTATIVE
        # =====================================================

        try:
            representative = verification.representative

        except VerificationRepresentative.DoesNotExist:
            raise ValueError(
                "No verification representative is associated "
                "with this verification request."
            )

        # =====================================================
        # 6. AUTHORIZED
        # =====================================================

        if decision == PropertyVerificationAuthorization.Decision.AUTHORIZED:
            # ---------------------------------------------
            # Validate authorization confirmations
            # ---------------------------------------------

            if not availability_confirmed:
                raise ValueError("Property availability must be confirmed.")

            if not agent_authorized:
                raise ValueError("Agent authorization must be confirmed.")

            # ---------------------------------------------
            # Create authorization record
            # ---------------------------------------------

            authorization = PropertyVerificationAuthorization.objects.create(
                verification=verification,
                decision=(PropertyVerificationAuthorization.Decision.AUTHORIZED),
                availability_confirmed=True,
                agent_authorized=True,
                authorization_note=authorization_note,
                rejection_reason="",
                responded_at=now,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            # ---------------------------------------------
            # Update representative
            # ---------------------------------------------

            representative.confirmed_identity = True
            representative.confirmed_authority = True

            representative.save(
                update_fields=[
                    "confirmed_identity",
                    "confirmed_authority",
                    "updated_at",
                ]
            )

            # ---------------------------------------------
            # Update verification
            # ---------------------------------------------

            verification.status = PropertyVerification.VerificationStatus.AUTHORIZED

            verification.authorized_at = now

            verification.save(
                update_fields=[
                    "status",
                    "authorized_at",
                    "updated_at",
                ]
            )

            return authorization

        # =====================================================
        # 7. REJECTED
        # =====================================================

        if decision == PropertyVerificationAuthorization.Decision.REJECTED:
            # ---------------------------------------------
            # Validate rejection reason
            # ---------------------------------------------

            rejection_reason = rejection_reason.strip()

            if not rejection_reason:
                raise ValueError("A rejection reason is required.")

            # ---------------------------------------------
            # Create rejection record
            # ---------------------------------------------

            authorization = PropertyVerificationAuthorization.objects.create(
                verification=verification,
                decision=(PropertyVerificationAuthorization.Decision.REJECTED),
                availability_confirmed=False,
                agent_authorized=False,
                authorization_note="",
                rejection_reason=rejection_reason,
                responded_at=now,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            # ---------------------------------------------
            # Update representative
            # ---------------------------------------------

            representative.confirmed_identity = False
            representative.confirmed_authority = False

            representative.save(
                update_fields=[
                    "confirmed_identity",
                    "confirmed_authority",
                    "updated_at",
                ]
            )

            # ---------------------------------------------
            # Update verification
            # ---------------------------------------------

            verification.status = PropertyVerification.VerificationStatus.REJECTED

            verification.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            return authorization
