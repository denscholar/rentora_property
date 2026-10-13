from django.urls import path

from accounts.views import (
    LoginAPIView,
    LogoutAPIView,
    MobileLoginAPIView,
    RegisterAPIView,
    ResendEmailOTPAPIView,
    ResendPhoneOTPAPIView,
    VerifyEmailOTPAPIView,
    VerifyPhoneOTPAPIView,
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path(
        "auth/verify-email-otp/",
        VerifyEmailOTPAPIView.as_view(),
        name="verify-email-otp",
    ),
    path(
        "auth/verify-otp-mobile/",
        VerifyPhoneOTPAPIView.as_view(),
        name="verify-phone-otp",
    ),
    path(
        "auth/resend-otp-mobile/",
        ResendPhoneOTPAPIView.as_view(),
        name="resent-otp",
    ),
    path(
        "auth/resend-email-otp/",
        ResendEmailOTPAPIView.as_view(),
        name="resend-email-otp",
    ),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "mobile/login/",
        MobileLoginAPIView.as_view(),
        name="mobile-login",
    ),
]
