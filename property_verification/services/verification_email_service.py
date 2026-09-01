from django.utils import timezone
import resend

from django.conf import settings
from django.template.loader import render_to_string

from resend.exceptions import ResendError


class PropertyVerificationEmailService:
    """
    Handles emails related to property verification.
    """

    TEMPLATE = "property_verification/" "verification_invitation.html"

    @classmethod
    def send_verification_invitation(
        cls,
        *,
        verification,
        verification_url: str,
    ):
        """
        Send the property verification invitation.

        Returns:
            Resend email response.
        """

        if not settings.RESEND_API_KEY:
            raise RuntimeError("RESEND_API_KEY is not configured.")

        if not verification.representative.email:
            raise ValueError("Representative email is required.")

        resend.api_key = settings.RESEND_API_KEY

        representative_name = (
            verification.representative.name or "Property Representative"
        )

        property_reference = str(verification.submission.uuid)

        html = render_to_string(
            cls.TEMPLATE,
            {
                "representative_name": representative_name,
                "verification_url": verification_url,
                "property_reference": property_reference,
            },
        )

        params: resend.Emails.SendParams = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [verification.representative.email],
            "subject": ("Action Required: " "Verify Property on SheltaMe"),
            "html": html,
        }

        options: resend.Emails.SendOptions = {
            "idempotency_key": (
                "property-verification-invitation/" f"{verification.uuid}"
            ),
        }

        try:
            email = resend.Emails.send(
                params,
                options,
            )

            verification.email_status = verification.EmailStatus.SENT

            verification.email_sent_at = timezone.now()

            verification.email_provider_id = email.id

            verification.email_error = ""

            verification.save(
                update_fields=[
                    "email_status",
                    "email_sent_at",
                    "email_provider_id",
                    "email_error",
                    "updated_at",
                ]
            )

            return email

        except ResendError as error:

            verification.email_status = verification.EmailStatus.FAILED

            verification.email_error = str(error)

            verification.save(
                update_fields=[
                    "email_status",
                    "email_error",
                    "updated_at",
                ]
            )

            raise
