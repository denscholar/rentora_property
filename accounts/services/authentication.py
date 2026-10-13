from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


# ==========================================
# AUTHENTICATE USER - Email
# ==========================================
def authenticate_user(request, email, password):
    user = authenticate(
        request=request,
        username=email,
        password=password,
    )

    if not user:
        raise ValidationError("Invalid email or password.")

    if not user.is_active:
        raise ValidationError("This account has been disabled.")

    if not user.is_verified:
        raise ValidationError("Please verify your email before logging in.")

    return user


# ==========================================
# AUTHENTICATE USER - Email
# ==========================================
def authenticate_user_phone(request, phone_number, password):
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
    except CustomUser.DoesNotExist:
        raise ValidationError("Invalid phone_number or password.")

    if not user.check_password(password):
        raise ValidationError("Invalid phone_number or password.")

    if not user.is_active:
        raise ValidationError("This account has been disabled.")

    if not user.is_verified:
        raise ValidationError("Please verify your phone_number before logging in.")

    return user


# ==========================================
# LOGIN USER
# ==========================================
def login_user(request, user):
    login(request, user)
    return user


# ==========================================
# LOGOUT USER
# ==========================================
def logout_user(request):
    logout(request)
