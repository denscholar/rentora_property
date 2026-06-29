import random
from datetime import timedelta

from django.utils import timezone


# ==========================================
# GENERATE EMAIL OTP
# ==========================================
def generate_email_otp(user):
    otp = str(random.randint(100000, 999999))

    user.email_otp = otp
    user.email_otp_expires_at = timezone.now() + timedelta(minutes=10)

    user.save(
        update_fields=[
            "email_otp",
            "email_otp_expires_at",
            "updated_at",
        ]
    )

    return otp


# ==========================================
# VALIDATE EMAIL OTP
# ==========================================
def validate_email_otp(user, otp):
    if not user.email_otp:
        return False

    if user.email_otp != otp:
        return False

    if not user.email_otp_expires_at:
        return False

    if timezone.now() >= user.email_otp_expires_at:
        return False

    return True


# ==========================================
# MARK EMAIL VERIFIED
# ==========================================
def mark_email_verified(user):
    now = timezone.now()

    user.is_verified = True
    user.email_otp = None
    user.email_otp_expires_at = None
    user.email_otp_verified_at = now
    user.email_verified_at = now

    user.save(
        update_fields=[
            "is_verified",
            "email_otp",
            "email_otp_expires_at",
            "email_otp_verified_at",
            "email_verified_at",
            "updated_at",
        ]
    )

    return user