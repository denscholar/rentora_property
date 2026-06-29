from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError


# ==========================================
# AUTHENTICATE USER
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