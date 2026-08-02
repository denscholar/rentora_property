from django.urls import path

from accounts.views import (
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    ResendEmailOTPAPIView,
    VerifyEmailOTPAPIView,
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/verify-email-otp/", VerifyEmailOTPAPIView.as_view(), name="verify-email-otp"),
    path("auth/resend-email-otp/", ResendEmailOTPAPIView.as_view(), name="resend-email-otp"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
]
