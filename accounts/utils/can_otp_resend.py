from django.utils import timezone
from datetime import timedelta

from accounts.constants import (
    MAX_PHONE_OTP_RESEND_ATTEMPTS,
    PHONE_OTP_RESEND_LOCK_HOURS,
)

now = timezone.now()

def can_resend_otp(user):

    # User is currently locked
    if (
        user.phone_otp_resend_locked_until
        and user.phone_otp_resend_locked_until > now
    ):
        return False

    return True


def increment_otp_resend_attempt(user):
    user.otp_resend_count += 1
    user.otp_created_at = now

    if user.otp_resend_count >= MAX_PHONE_OTP_RESEND_ATTEMPTS:
        user.otp_resend_locked_until = timezone.now() + timedelta(
            hours=PHONE_OTP_RESEND_LOCK_HOURS
        )

        # Reset count after lock
        user.phone_otp_resend_count = 0

    user.save(
        update_fields=[
            "otp_resend_count",
            "otp_resend_locked_until",
            "otp_created_at",
            "updated_at",
        ]
    )