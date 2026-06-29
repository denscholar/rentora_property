from django.db import transaction
from accounts.models import CustomUser
from accounts.services.otp import generate_email_otp
from accounts.services.email import send_email_otp


# ==========================================
# REGISTER USER
# ==========================================
@transaction.atomic
def register_user(validated_data):
    password = validated_data.pop("password")
    validated_data.pop("confirm_password")

    user = CustomUser.objects.create(
        **validated_data,
        is_active=True,
        is_verified=False,
    )

    user.set_password(password)
    user.save(update_fields=["password"])

    otp = generate_email_otp(user)
    send_email_otp(user, otp)

    return user