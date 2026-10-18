from django.db import transaction
from django.utils import timezone
from accounts.models import CustomUser
from accounts.services.email import send_email_otp
from accounts.services.termii_sms_service import TermiiService


@transaction.atomic
def register_user(validated_data):
    data = dict(validated_data)

    password = data.pop("password")
    data.pop("confirm_password", None)

    email = data.pop("email", None)

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        **data,
        is_active=True,
        is_verified=False,
    )

    if user.role == CustomUser.Role.TENANT:
        now = timezone.now()
        otp = user.generate_phone_otp()
        user.otp_created_at = now

        user.save(
            update_fields=[
                "otp_created_at",
            ]
        )

        TermiiService.send_sms(
            phone_number=user.phone_number,
            otp=otp,
        )

    else:
        otp = user.generate_email_otp()
        send_email_otp(user, otp)

    return user
