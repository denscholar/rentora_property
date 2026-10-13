from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from accounts.models import CustomUser


def authenticate_tenant_by_phone(
    request,
    phone_number,
    password,
):
    user = authenticate(
        request=request,
        phone_number=phone_number,
        password=password,
    )

    if not user or user.role != CustomUser.Role.TENANT:
        raise ValidationError("Invalid phone number or password.")

    return user
